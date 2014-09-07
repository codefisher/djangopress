from django.core.management.base import BaseCommand
from djangopress.forum.models import Thread, Post, Forum

class Command(BaseCommand):
    help = 'Fixes the counts on threads and forums'

    def handle(self, *args, **options):
        for thread in Thread.objects.all():
            Thread.objects.filter(pk=thread.pk).update(num_posts=Post.objects.filter(thread=thread.pk, is_spam=False, is_public=True).count())
        for forum in Forum.objects.all():
            try:
                Forum.objects.filter(pk=forum.pk).update(num_posts=Post.objects.filter(thread__forum=forum.pk, is_spam=False, is_public=True).count())
                Forum.objects.filter(pk=forum.pk).update(num_threads=Thread.objects.filter(forum=forum.pk).exclude(last_post=None).count())
            except:
                pass # empty forum