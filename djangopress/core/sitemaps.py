
class SitemapRegister(object):

    sitemaps = {}

    def __call__(self, name, cls):
        SitemapRegister.sitemaps[name] = cls

    def get_sitemaps(self):
        return self.sitemaps

register = SitemapRegister()