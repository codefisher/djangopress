import re
from bbcode import Lexer, Parser
from djangopress.core.format import nodes
from django.conf import settings

TAG_START = "<"
TAG_END = ">"

class MagicLibrary(nodes.Library):
    tags = {}

class HtmlLexer(Lexer):
    TAG_START = TAG_START
    TAG_END = TAG_END
    tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)))

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

if __name__ == "__main__":
    print magic_html("""
        <script>alert('hit'); </script>
        <h2 onclick="alert('hit')"><image src="/static/images/icons/toolbar-buttons.png" width="32" height="32" alt=""><a href="#">Toolbar Buttons</a></h2>
        <p>
          <a href="#">Toolbar Buttons</a> is a <b>button</b> set for several applications including Firefox, Thunerbird and Sunbird.  It boast over 100 buttons for Firefox alone.  This easily makes it the largest set available. It does everything from opening the Add-ons manager, bookmarking pages or translating them, to restarting the application or disabling JavaScript.  There have been over 1 million downloads to date.
        </p>

        <ul>
            <li>Item one <ul><li>Stuff</li></ul></li>
            <li>Item two </li>
            <li>Item three
            <li>Item four </li>
        </ul>

        <dl>
            <dt>One</dt>
            <dd>item</dd>
        </dl>
        """)