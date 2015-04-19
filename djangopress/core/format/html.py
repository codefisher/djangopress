
import lxml
import html5lib
from lxml import html
from html5lib import sanitizer
from html5lib.constants import tokenTypes

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class Library(object):
    tags = {}

    @classmethod
    def tag(cls, name=None, func=None):
        cls.tags[name] = func

def format_code(node):
    if not node.attrib.get('codelang'):
        return None
    lexer = get_lexer_by_name(node.attrib.get('codelang'), stripall=True)
    formatter = HtmlFormatter(linenos=True)
    code = node.text + ''.join(html.tostring(n) for n in node)
    result = highlight(code, lexer, formatter)
    code_node = html.fromstring(result)
    return code_node

Library.tag("//code", format_code)

def extended_html(text, *args, **kwargs):
    nodes = html.fragment_fromstring(text, create_parent='div')
    for name, func in Library.tags.items():
        for n in nodes.xpath(name):
            new = func(n)
            if new is not None:
                n.getparent().replace(n, new)
    return ''.join(html.tostring(node) for node in nodes)

class StripSanitizer(sanitizer.HTMLSanitizer):
    def disallowed_token(self, token, token_type):
        return None

def sanatized_html(text):
    p = html5lib.HTMLParser(tokenizer=StripSanitizer)
    doc = p.parseFragment(text)
    walker = html5lib.getTreeWalker("etree")
    stream = walker(doc)
    s = html5lib.serializer.HTMLSerializer()
    output = s.serialize(stream)
    return ''.join(output)