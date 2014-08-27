from django.db import models

class EntryMananger(models.Manager):

    def get_entries(self, blog=None, ordered=True):
        entry_list = self.select_related('blog', 'author').filter(status="PB", visibility="VI")
        if blog is not None:
            entry_list = entry_list.filter(blog=blog)
        if ordered:
            return entry_list.order_by('-sticky', '-posted')
        return entry_list
    
class CategoryMananger(models.Manager):

    def get_categories(self, blog=None, ordered=True):
        categories_list = self.select_related('blog', 'parent_category').all()
        if blog is not None:
            categories_list = categories_list.filter(blog=blog)
        if ordered:
            return categories_list.order_by('name')
        return categories_list