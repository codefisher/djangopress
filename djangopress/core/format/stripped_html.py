import re
from djangopress.core.format.parser import Lexer, Parser, encode_html
from djangopress.core.format.nodes import Library, Node, tag_arguments, render, AttrNode
from django.utils.safestring import mark_safe


TAG_START = "&lt;"
TAG_END = "&gt;"

class StrippedLibrary(Library):
    tags = {}

    @classmethod
    def tagless(self, tag_name, block=False, can_contain_self=True, stop_at=None):
        """
        tag_name - name of the code tag
        node_name - name of the html code tag
        """
        if stop_at == None:
            stop_at = ()
        def func(parser, token):
            _, arg, kargs = tag_arguments(token.contents)
            if can_contain_self:
                nodelist = parser.parse(('/%s' % tag_name,) + stop_at)
            else:
                nodelist = parser.parse(('/%s' % tag_name, tag_name) + stop_at)
            name = tag_arguments(parser.tokens[0].contents)[0]
            if name == '/%s' % tag_name:
                parser.delete_first_token()
            return TagLessNode(token, block, nodelist, kargs)
        self.tag(tag_name, func)
        
class TagLessNode(Node):

    def __init__(self, token, block, nodelist, kargs):
        super(TagLessNode, self).__init__(token)
        self.block = block
        self.nodelist = nodelist
        self.kargs = kargs
        
    def render(self, context, ids=None, **kwargs):
        if ids and self.kargs.get('id') in ids:
            return ''
        if self.block:
            return mark_safe("\n%s\n" % self.nodelist.render(context, ids=ids, **kwargs))
        return mark_safe(" %s " % self.nodelist.render(context, ids=ids, **kwargs))
    
class TagLessAttrNode(AttrNode):
    def render(self, context, **kwargs):
        data = self._render(context, **kwargs)
        if type(data) == dict:
            return render(''' {% for attr, value in attrs.items %} {{value}} {% endfor %}{% if closes %} {{ content }} {% endif %} ''', data)
        return data
    
# it is worth noting that if a tag is not know, it is simply dropped, and does not appear in the output
for tag in ['title', 'address', 'big', 'cite', 'code', 'del', 'dfn', 'span', 'b', 'i', 'strike', 's'
            'em', 'ins', 'kbd', 'p', 'pre', 'q', 'samp', 'small', 'strong', 'sub', 'sup', 'tt', 'var', 'ins']:
    StrippedLibrary.tagless(tag)
    
for tag in ['fieldset', 'form', 'legend', 'div', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'dl', 'dd', 'dt', 'table', 'tr', 'td', 'th', 'thead', 'tfoot', 'tbody', 'caption' ]:
    StrippedLibrary.tagless(tag, block=True)

for tag, attrs in [('abbr', ('title',)), ('a', ('title',)), ('acronym', ('title',)), ('bdo', ('dir',))]:
    StrippedLibrary.attr_tag(tag, attrs=attrs, cls=TagLessAttrNode)
StrippedLibrary.attr_tag("img", attrs=('alt', 'title'), closes=False, cls=TagLessAttrNode)


# these tags and their content are striped out
for tag in ['applet', 'button', 'frame', 'frameset',
            'object', 'select', 'style', 'script', 'video', 'audio']:
    StrippedLibrary.comment_tag(tag)

class HtmlLexer(Lexer):
    TAG_START = TAG_START
    TAG_END = TAG_END
    tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)), re.DOTALL)

def stripped_html(text, context=None, ids=None, *args, **kargs):
    text = encode_html(re.sub(r'&#?\w+;', '', text))
    lex = HtmlLexer(text)
    parse = Parser(lex.tokenize())
    parse.tags = StrippedLibrary
    return parse.parse().render(context, ids=ids)
