import re
from django.utils.safestring import mark_safe
from bbcode import Lexer, Parser, encode_html
from nodes import Library, TagNode, tag_arguments, def_list_func

TAG_START = "&lt;"
TAG_END = "&gt;"

register = Library()

# these are considered safe, and allowed in the output.  Note that all attributes
# are ignored.
for tag in ['address', 'big', 'blockquote', 'cite', 'code', 'del', 'dfn',
            'div', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ins', 'kbd',
            'p', 'pre', 'q', 'samp', 'small', 'span', 'strong', 'sub', 'sup',
            'tt', 'var']:
    register.simple_tag(tag)
for tag in ['br', 'hr']:
    pass

#these nodes are transformed into other equivalent nodes
for tag, node in [('b', 'strong'), ('i', 'em'), ('strike', 'del'), ('s', 'del'), ]:
    register.simple_tag(tag, node)

#these tags are kept along with select attributes
for tag, attrs in [('abbr', ('title',)), ('acronym', ('title',)), ('bdo', ('dir',))]:
    register.attr_tag("abbr", attrs=attrs)

# these tags and their content are striped out
for tag in ['applet', 'button', 'fieldset', 'form', 'frame', 'frameset',
            'head', 'object', 'select', 'style', 'script', 'video', 'audio']:
    register.comment_tag(tag)

#dl, ol, ul, table

register.link_tag("img", link_arg='src',
        attrs=("src", "width", "height", "alt", "title"), closes=False)
register.link_tag('a', link_arg='href', attrs=('title', 'href'))

register.tag('dl', def_list_func)

class ListNode(TagNode):
    def __init__(self, token, arg, items, tag):
        super(ListNode, self).__init__(token)
        self.arg = arg
        self.items = items
        self.tag = tag

    def render(self, context):
        data = {
            "tag": self.tag,
            "items": "".join("<li>%s</li>" % item.render(context)
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

register.tag('ul', list_func)
register.tag('ol', list_func)

class HtmlLexer(Lexer):
    TAG_START = TAG_START
    TAG_END = TAG_END
    tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)))

def sanitized_html(text, context=None, *args, **kargs):
    text = encode_html(text)
    lex = HtmlLexer(text)
    parse = Parser(lex.tokenize())
    parse.add_library(register)
    return parse.parse().render(context)

if __name__ == "__main__":
    print sanitized_html("""
        <script>alert('hit'); </script>
        <h2 onclick="alert('hit')"><img src="/media/images/icons/toolbar-buttons.png" width="32" height="32" alt=""><a href="#">Toolbar Buttons</a></h2>
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