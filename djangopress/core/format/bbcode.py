
from djangopress.core.format.nodes import TagNode, Library, tag_arguments
from djangopress.core.format.parser import Parser, Lexer, encode_html
from django.utils.html import urlize
from djangopress.core.format.smilies import add_smilies
from djangopress.core.format.nodes import def_list_func

register = Library()

TAG_START = '['
TAG_END = ']'
#tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)))

class CodeNode(TagNode):
    def __init__(self, token, nodelist):
        super(CodeNode, self).__init__(token)
        self.nodelist = nodelist

    def render(self, context):
        return "<pre><code>%s</code></pre>" % self.nodelist.contents()

@register.tag()
def code(parser, token):
    nodelist = parser.parse(('/code',), collect=True)
    parser.delete_first_token()
    return CodeNode(token, nodelist)

for tag in ["url", "link"]:
    register.link_tag(tag, link_arg='href', node_name='a',
        arg_name='href', attrs=('title', ))
for tag in ["img", "image"]:
    register.link_tag(tag, link_arg='src', node_name='img', arg_name="src",
            attrs=("width", "height", "alt", "title"), closes=False, content_attr="alt")

class ListNode(TagNode):
    def __init__(self, token, arg, items):
        super(ListNode, self).__init__(token)
        self.arg = arg
        self.items = items

    def render(self, context):
        # self.arg could be '1' or 'a'
        data = {
            "tag": 'ol' if self.arg else 'ul',
            "items": "".join("<li>%s</li>" % item.render(context)
                            for item in self.items),
            "alpha": self.arg == "a"
        }
        return '<%(tag)s{% if alpha %} style="list-style-type:lower-alpha"{% endif %}>%(items)s</%(tag)s>' % data

def list_func(parser, token):
    tag, arg, _ = tag_arguments(token.contents)
    if tag == 'ol':
        arg = '1'
    items = []
    nodelist = parser.parse(('/%s' % tag, '*', 'li'))
    while parser.tokens[0].contents != '/%s' % tag:
        parser.delete_first_token()
        nodelist = parser.parse(('/%s' % tag, '*', 'li'))
        items.append(nodelist)
    parser.delete_first_token()
    return ListNode(token, arg, items)

register.tag('list', list_func)
register.tag('ul', list_func)
register.tag('ol', list_func)

register.tag('dl', def_list_func)

register.argumented_tag('color', '<span style="color:{{ arg }};">{{ content }}</span>')
register.argumented_tag('size', '<span style="font-size:{{ arg }}%;">{{ content }}</span>')
register.simple_tag("b", "strong")
register.simple_tag("i", "em")
register.simple_tag("s", "del")
register.simple_tag("u")

register.attr_tag("abbr", arg_name="title")
register.attr_tag("acronym", arg_name="title")
register.unclosed_tag("hr")

#to be added: email, quote, table

def bbcode(text, context=None, nofollow=True, trim_url_limit=None, smilies=True, *args, **kargs):
    text = encode_html(text)
    lex = Lexer(text)
    parse = Parser(lex.tokenize())
    parse.add_library(register)
    return add_smilies(urlize(parse.parse().render(context),
            nofollow=nofollow, trim_url_limit=trim_url_limit), smilies=smilies)

if __name__ == "__main__":
    print bbcode("""
    [url=http://codefisher.org/ title="My Home Page"][b]www.codefisher.org[/b][/url]

    [url=/forum]Forum[/url]
    [url=www.google.com]Google[/url]
    [url=javascript:alert('hit')]Google[/url]

    <script>alert('hit'); </script>
    [list]
    [*] [color=red][i]One[/i][/color]
    [*] Two
    [*] [url]google.com[/url]
    [/list]

    [img="http://codefisher.org/img.png" width="30" height="40" foo="bar"]
    [img=http://codefisher.org/img.png]Some text[/img]
    [hr]
    [code]What [i] is that [/i][/code] www.code.com

    [B] [i]I what help http://codefisher.org/ [/B][/i]

    """)
