from django.db import models

class EntryMananger(models.Manager):

    def get_entries(self, blog=None):
        entry_list = self.select_related('blog', 'author').filter(status="PB", visibility="VI")
        if blog is not None:
            entry_list = entry_list.filter(blog=blog)
        if sorted:
            return entry_list.order_by('-sticky', '-posted')
        return entry_list