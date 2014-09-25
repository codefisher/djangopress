from haystack import indexes
from djangopress.pages.models import Page

class PagesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='edited')
    title = indexes.CharField(model_attr='title', boost=1.5)

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status="PB", visibility="VI")
    
    def prepare(self, obj):
        data = super(PagesIndex, self).prepare(obj)
        data['boost'] = 1.5
        return data
