from django.core.management.base import BaseCommand
from djangopress.forum.models import Thread, Post, Forum
import time
import akismet
from django.conf import settings
from django.utils.encoding import force_str


class Command(BaseCommand):
    help = 'Check if any posts are spam and marks them as such'

    def handle(self, *args, **options):
        try:
            api = akismet.Akismet(key=settings.AKISMET_API.get('key'),
                              blog_url=settings.AKISMET_API.get('blog_url'))
        except akismet.ConfigurationError as e:
            print("Akismet is not configured correctly")
        except akismet.APIKeyError as e:
            print("Not using a valid key")
        for post in Post.objects.filter(is_spam=False):
            data = {
                "user_ip": post.ip,
            }
            if post.author:
                data.update({
                    "comment_author": post.author.username,
                    "comment_author_email": post.author.email,
                    "comment_author_url": post.author.profile.homepage,
                })
            else:
                data.update({
                    "comment_author": post.poster_name,
                    "comment_author_email": post.poster_email,
                })
            if api.comment_check(force_str(post.message), data):
                post.is_spam = True
                post.save()
                print("Post {} was spam.".format(post.pk))
            else:
                print("Post {} was not spam.".format(post.pk))
            time.sleep(2)