import datetime
from haystack import site, indexes
from djangopress.blog.models import Entry


class EntryIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='posted')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Entry.get_entries(sorted=False)

site.register(Entry, EntryIndex)
