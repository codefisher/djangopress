from djangopress.core import format

class RenderRegister(object):

    def __init__(self):
        self._func = {}
        self._choices = {}

    def __call__(self, name, func, verbose_name):
        self._func[name] = func
        self._choices[name] = verbose_name
        
    def choices(self):
        return self._choices.items()

    def render(self, block, name, data, context):
        func = self._func.get(name)
        if func:
            return func(block, data, context)
        return ''

register = RenderRegister()

for name, verbose_name in format.Library.choices(False):
    register(name, lambda block, data, context: format.Library.format(name, data, False, context=context), verbose_name)