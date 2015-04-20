from djangopress.core.format import library

class RenderRegister(object):

    def __init__(self):
        self._func = {}
        self._choices = {}

    def __call__(self, name, func, verbose_name):
        self._func[name] = func
        self._choices[name] = verbose_name
        
    def choices(self):
        return list(self._choices.items())

    def render(self, block, name, data, context):
        func = self._func.get(name)
        if func:
            return func(block, data, context)
        return ''

register = RenderRegister()

def make_render(name):
    return lambda block, data, context: library.Library.format(name, data, False, context=context)

for name, verbose_name in library.Library.choices(False):
    register(name, make_render(name), verbose_name)