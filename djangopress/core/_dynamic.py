
class DynamicRegister(object):

    def __init__(self):
        self._modules = {}

    def __call__(self, name, func, mod):
        self._modules[name] = (func, mod)

    def get_modules(self):
        return self._modules

register = DynamicRegister()