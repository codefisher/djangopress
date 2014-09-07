from django.core.management.base import BaseCommand
from djangopress.forum.models import Thread, Post, Forum

class Command(BaseCommand):
    help = 'Fixes the last and first post on threads and forums'

    def handle(self, *args, **options):
        #fix Thread first_post, last_post, last_post_date, 
        #fix Forum last_post
        for thread in Thread.objects.all():
            Thread.objects.filter(pk=thread.pk).update(first_post=Post.objects.filter(thread=thread.pk, is_spam=False, is_public=True).order_by('posted')[0])
            Thread.objects.filter(pk=thread.pk).update(last_post=Post.objects.filter(thread=thread.pk, is_spam=False, is_public=True).order_by('-posted')[0])
        for forum in Forum.objects.all():
            try:
                Forum.objects.filter(pk=forum.pk).update(last_post=Post.objects.filter(thread__forum=forum.pk, is_spam=False, is_public=True).order_by('-posted')[0])
            except:
                pass # empty forum
