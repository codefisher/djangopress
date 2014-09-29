from djangopress.core.search import ModelSetSearchView
from djangopress.forum.views import get_forum

class ForumSearchView(ModelSetSearchView):
    
    def __init__(self, *args, **kwargs):
        self.forums = None
        super(ForumSearchView, self).__init__(*args, **kwargs)
        
    def __call__(self, request, forums_slug, *args, **kwargs):
        self.forums = get_forum(forums_slug)
        return super(ForumSearchView, self).__call__(request)
    
    def extra_context(self):
        return {
            'forums': self.forums,
        }