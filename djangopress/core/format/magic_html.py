import re
from .bbcode import Lexer, Parser
from . import nodes
from django.conf import settings

TAG_START = "<"
TAG_END = ">"

class MagicLibrary(nodes.Library):
    tags = {}

class HtmlLexer(Lexer):
    TAG_START = TAG_START
    TAG_END = TAG_END
    tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)), re.DOTALL)

class HtmlTagNode(nodes.TagNode):
    def render(self, context, **kwargs):
        return self.contents()

class MagicHtmlParser(Parser):
    def parse_error(self, nodelist, token):
        self.extend_nodelist(nodelist, HtmlTagNode(token))

def image_tag(parser, token):
    kargs = nodes.tag_arguments(token.contents)[2]
    kargs["src"] = "%s/%s" % (settings.STATIC_URL.rstrip('/'),
            kargs.get("src").lstrip('/'))
    return nodes.AttrNode(token, node_name="img", kargs=kargs, closes=False,
                    attrs=('src', 'width', 'height', 'title', 'alt'))
MagicLibrary.tag("image", image_tag)

def magic_html(text, context=None, *args, **kargs):
    lex = HtmlLexer(text)
    parse = MagicHtmlParser(lex.tokenize())
    parse.tags = MagicLibrary
    return parse.parse().render(context)