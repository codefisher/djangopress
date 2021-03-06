from haystack import indexes
from djangopress.blog.models import Entry

class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='posted')
    title = indexes.CharField(model_attr='title', boost=1.5)

    def get_model(self):
        return Entry

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.get_entries(ordered=False)
    
    def prepare(self, obj):
        data = super(EntryIndex, self).prepare(obj)
        data['boost'] = 1
        return data
