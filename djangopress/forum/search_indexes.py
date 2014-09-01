from haystack import indexes
from djangopress.forum.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='message', document=True, use_template=True, boost=0.25)
    author = indexes.CharField(model_attr='author_name')
    pub_date = indexes.DateTimeField(model_attr='posted')
    title = indexes.CharField(model_attr='thread__subject', boost=1)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_spam=False, is_public=True)

    def prepare(self, obj):
        data = super(PostIndex, self).prepare(obj)
        data['boost'] = 0.0
        return data
        