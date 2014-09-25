from haystack.forms import SearchForm
from haystack.views import SearchView
from django.db import models

class ModelSetSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        self.models = kwargs["models"]
        del kwargs["models"]
        super(ModelSetSearchForm, self).__init__(*args, **kwargs)

    def get_models(self):
        search_models = []
        for model in self.models:
            search_models.append(models.get_model(*model.split('.')))
        return search_models

    def search(self):
        sqs = super(ModelSetSearchForm, self).search()
        return sqs.models(*self.get_models())
    
class ModelSetSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        self.models = kwargs["models"]
        del kwargs["models"]
        super(ModelSetSearchView, self).__init__(*args, **kwargs)
        
    def __call__(self, request, *args, **kwargs):
        return super(ModelSetSearchView, self).__call__(request)
        
    def build_form(self, form_kwargs=None):
        if form_kwargs == None:
            form_kwargs = {}
        form_kwargs["models"] = self.models
        return super(ModelSetSearchView, self).build_form(form_kwargs)
    
def search_view_factory(view_class=SearchView, *args, **kwargs):
    '''
    This is a replacement for the original method from haystack.views
    that allows the url() to pass parameters to the view
    '''
    def search_view(request, *vargs, **vkwargs):
        return view_class(*args, **kwargs)(request, *vargs, **vkwargs)
    return search_view