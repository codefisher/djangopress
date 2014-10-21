
from djangopress.core.format.nodes import TagNode, Library, tag_arguments, TextNode, LinkNode
from djangopress.core.format.parser import Parser, Lexer, encode_html
from django.utils.html import urlize
from djangopress.core.format.smilies import add_smilies
from djangopress.core.format.nodes import def_list_func

class BBcodeLibrary(Library):
    tags = {}

TAG_START = '['
TAG_END = ']'
#tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)))

class BBcodeImg(LinkNode):
    def render(self, context, show_images=True, **kwargs):
        if not show_images:
            return self.kargs.get("alt", "")
        return super(BBcodeImg, self).render(context, **kwargs)

class BBcodeLink(LinkNode):
    def render(self, context, render_links=True, **kwargs):
        if not render_links:
            data = self._render(context, **kwargs)
            return "%s (%s)" % (data.get("content"), data.get("attrs").get("href"))
        return super(BBcodeLink, self).render(context, **kwargs)

class BBcodeText(TextNode):
    def render(self, context, nofollow=True, trim_url_limit=None, smilies=True, should_urlize=True, **kwargs):
        if smilies:
            text = add_smilies(self.token.contents)
        else:
            text = self.token.contents
        if should_urlize:
            text = urlize(text, nofollow=nofollow, trim_url_limit=trim_url_limit)
        return add_line_breaks(text)

class BBcodeParser(Parser):
    def create_text(self, nodelist, token):
        self.extend_nodelist(nodelist, BBcodeText(token))

def add_line_breaks(text):
    return text.replace("\n", "<br />")

class CodeNode(TagNode):
    def __init__(self, token, nodelist):
        super(CodeNode, self).__init__(token)
        self.nodelist = nodelist

    def render(self, context, **kwargs):
        return """<div class="code"><pre><code>%s</code></pre></div>""" % self.nodelist.contents()

@BBcodeLibrary.tag()
def code(parser, token):
    nodelist = parser.parse(('/code',), collect=True)
    parser.delete_first_token()
    return CodeNode(token, nodelist)

for tag in ["url", "link"]:
    BBcodeLibrary.link_tag(tag, link_arg='href', node_name='a',
        arg_name='href', attrs=('title', ), cls=BBcodeLink)
for tag in ["img", "image"]:
    BBcodeLibrary.link_tag(tag, link_arg='src', node_name='img', arg_name="src",
            attrs=("width", "height", "alt", "title"), closes=False, content_attr="alt", cls=BBcodeImg)

class ListNode(TagNode):
    def __init__(self, token, arg, items):
        super(ListNode, self).__init__(token)
        self.arg = arg
        self.items = items

    def render(self, context, **kwargs):
        # self.arg could be '1' or 'a'
        data = {
            "tag": 'ol' if self.arg else 'ul',
            "items": "".join("<li>%s</li>" % add_line_breaks(item.render(context, **kwargs).strip())
                            for item in self.items),
            "attrs": ''' style="list-style-type:lower-alpha"''' if self.arg == "a" else ''
        }
        return '<%(tag)s%(attrs)s>%(items)s</%(tag)s>' % data

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

BBcodeLibrary.tag('list', list_func)
BBcodeLibrary.tag('ul', list_func)
BBcodeLibrary.tag('ol', list_func)

BBcodeLibrary.tag('dl', def_list_func)

BBcodeLibrary.argumented_tag('color', '<span style="color:{{ arg }};">{{ content }}</span>')
BBcodeLibrary.argumented_tag('size', '<span style="font-size:{{ arg }}%;">{{ content }}</span>')
BBcodeLibrary.simple_tag("b", "strong")
BBcodeLibrary.simple_tag("i", "em")
BBcodeLibrary.simple_tag("s", "del")
BBcodeLibrary.simple_tag("u")

BBcodeLibrary.attr_tag("abbr", arg_name="title")
BBcodeLibrary.attr_tag("acronym", arg_name="title")
BBcodeLibrary.unclosed_tag("hr")

#to be added: email, quote, table

def bbcode(text, context=None, nofollow=True, trim_url_limit=None, smilies=True, should_urlize=True, **kargs):
    text = encode_html(text)
    lex = Lexer(text.strip())
    parse = BBcodeParser(lex.tokenize())
    parse.tags = BBcodeLibrary
    return parse.parse().render(context, nofollow=nofollow, trim_url_limit=trim_url_limit, 
                                smilies=smilies, should_urlize=should_urlize, **kargs)

if __name__ == "__main__":
    text = bbcode("""
    [url=http://codefisher.org/ title="My Home Page"][b]www.codefisher.org[/b][/url]

    [url=/forum]Forum[/url]
    [url=www.google.com]Google[/url]
    [url=javascript:alert('hit')]Google[/url]

    <script>alert('hit'); </script>
    [list]
    [*] [color=red][i]One[/i][/color]
    [*] Two

    Three
    [*] [url]google.com[/url]
    [/list]

    Once upon a time there was lots of text that needed to be formated correctly.

    [img="http://codefisher.org/img.png" width="30" height="40" foo="bar"]
    [img=http://codefisher.org/img.png]Some text[/img]
    [hr]
    [code]What [i] is that www.google.com [/i]
    that[/code] www.code.com

    [B] [i]I what help http://codefisher.org/ [/B][/i] that should be something that I need to build into

    """)
    print text
    open("text.html", "w").write(text)