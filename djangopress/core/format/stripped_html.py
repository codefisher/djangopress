
import lxml
from lxml.html.clean import Cleaner

def stripped_html(text, context=None, ids=None, *args, **kargs):
    doc = lxml.html.fromstring(text)
    cleaner = Cleaner()
    doc = cleaner.clean_html(doc)
    if ids:
        for id in ids:
            for bad in doc.xpath("//*[@id='%s']" % id):
                bad.getparent().remove(bad)
    return doc.text_content()
