


from django.core.management.base import BaseCommand
from djangopress.forum.models import Thread, Post, Forum
import time
import akismet
from django.conf import settings
from django.utils.encoding import force_str


class Command(BaseCommand):
    help = 'Check if any posts are spam and marks them as such'

    def handle(self, *args, **options):
        Post.objects.filter(is_spam=True).delete()
        # now there might be threads without any posts
        for thread in Thread.objects.all():
            if Post.objects.filter(thread=thread.pk).count() == 0:
                thread.delete()
        print("Spam posts deleted")