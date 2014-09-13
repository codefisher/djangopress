import re
from bbcode import Lexer, Parser, encode_html
from nodes import Library, TagNode, tag_arguments, def_list_func, table_func

TAG_START = "&lt;"
TAG_END = "&gt;"

class SanitizedLibrary(Library):
    tags = {}

# these are considered safe, and allowed in the output.  Note that all attributes
# are ignored.
for tag in ['address', 'big', 'blockquote', 'cite', 'code', 'del', 'dfn',
            'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ins', 'kbd', 'p', 'pre',
            'q', 'samp', 'small', 'strong', 'sub', 'sup', 'tt', 'var']:
    SanitizedLibrary.simple_tag(tag)
for tag in ['div', 'span']:
    SanitizedLibrary.simple_tag(tag, can_contain_self=True)

for tag in ['br', 'hr']:
    SanitizedLibrary.unclosed_tag(tag)

#these nodes are transformed into other equivalent nodes
for tag, node in [('b', 'strong'), ('i', 'em'), ('strike', 'del'), ('s', 'del'), ]:
    SanitizedLibrary.simple_tag(tag, node)

#these tags are kept along with select attributes
for tag, attrs in [('abbr', ('title',)), ('acronym', ('title',)), ('bdo', ('dir',))]:
    SanitizedLibrary.attr_tag(tag, attrs=attrs)

# these tags and their content are striped out
for tag in ['applet', 'button', 'fieldset', 'form', 'frame', 'frameset',
            'head', 'object', 'select', 'style', 'script', 'video', 'audio']:
    SanitizedLibrary.comment_tag(tag)

#dl, ol, ul, table

SanitizedLibrary.link_tag("img", link_arg='src',
        attrs=("src", "width", "height", "alt", "title"), closes=False)
SanitizedLibrary.link_tag('a', link_arg='href', attrs=('title', 'href'))

SanitizedLibrary.tag('dl', def_list_func)
SanitizedLibrary.tag('table', table_func)

class ListNode(TagNode):
    def __init__(self, token, arg, items, tag):
        super(ListNode, self).__init__(token)
        self.arg = arg
        self.items = items
        self.tag = tag

    def render(self, context, **kwargs):
        data = {
            "tag": self.tag,
            "items": "".join("<li>%s</li>" % item.render(context, **kwargs)
                            for item in self.items),
        }
        return '<%(tag)s>%(items)s</%(tag)s>' % data

def list_func(parser, token):
    tag, arg, _ = tag_arguments(token.contents)
    items = []
    nodelist = parser.parse(('/%s' % tag, 'li', '/li'))
    previous = ""
    while previous != '/%s' % tag:
        parser.delete_first_token()
        nodelist = parser.parse(('/%s' % tag, 'li', '/li'))
        if previous != "/li":
            items.append(nodelist)
        previous = parser.tokens[0].contents
    parser.delete_first_token()
    return ListNode(token, arg, items, tag)

SanitizedLibrary.tag('ul', list_func)
SanitizedLibrary.tag('ol', list_func)

class HtmlLexer(Lexer):
    TAG_START = TAG_START
    TAG_END = TAG_END
    tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)))

def sanitized_html(text, context=None, *args, **kargs):
    text = encode_html(text)
    lex = HtmlLexer(text)
    parse = Parser(lex.tokenize())
    parse.tags = SanitizedLibrary
    return parse.parse().render(context)

if __name__ == "__main__":
    print sanitized_html("""
        <script>alert('hit'); </script>
        <h2 onclick="alert('hit')"><img src="/static/images/icons/toolbar-buttons.png" width="32" height="32" alt=""><a href="#">Toolbar Buttons</a></h2>
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