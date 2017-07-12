from lxml import html

class Library(object):
    tags = {}

    @classmethod
    def tag(cls, name=None, func=None):
        cls.tags[name] = func

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter

    def format_code(node):
        if not node.attrib.get('codelang'):
            return None
        lexer = get_lexer_by_name(node.attrib.get('codelang'), stripall=True)
        formatter = HtmlFormatter(linenos=True)
        code = node.text + b''.join(map(bytes.decode, (html.tostring(n) for n in node)))
        result = highlight(code, lexer, formatter)
        code_node = html.fromstring(result)
        return code_node

    Library.tag("//code", format_code)
except ImportError:
    pass

def extended_html(text, *args, **kwargs):
    nodes = html.fragment_fromstring(text, create_parent='div')
    for name, func in Library.tags.items():
        for n in nodes.xpath(name):
            new = func(n)
            if new is not None:
                n.getparent().replace(n, new)
    return b''.join(map(bytes.decode, (html.tostring(node) for node in nodes)))