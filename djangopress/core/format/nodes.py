import re

from django.utils.safestring import mark_safe
from django.utils.text import smart_split
from django.template import Template, Context
from django.core.validators import URLValidator
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

def render(string, data):
    return Template(string).render(Context(data))

tag_name_re = re.compile('([^\w\*\-#])')

def tag_arguments(contents):
    def strip_quotes(value):
        if value.startswith('"') or value.startswith("'"):
            value = value[1:-1]
        return value
    contents = contents.strip()
    try:
        tag, split, args = tag_name_re.split(contents, 1)
    except ValueError:
        return contents, None, {}
    args = list(smart_split(args))
    has_anonymous = split == "="
    arg = strip_quotes(args[0]) if has_anonymous else ""
    kargs = {}
    for karg in args[int(has_anonymous):]:
        name, _, value = karg.partition('=')
        kargs[name] = strip_quotes(value)
    return tag, arg, kargs

class Library(object):

    def __init__(self):
        self.tags = {}
        self.libs = []

    def get(self, name):
        for lib in self.libs:
            tag = lib.get(name)
            if tag:
                return tag
        return self.tags[name]

    def push(self, lib):
        self.libs.insert(0, lib)

    def pop(self):
        self.libs.pop(0)

    def tag(self, name=None, compile_func=None):
        if compile_func:
            self.tags[name] = compile_func
        else:
            def _tag(compile_func):
                if name:
                    self.tags[name] = compile_func
                else:
                    self.tags[compile_func.__name__] = compile_func
            return _tag

    def simple_tag(self, tag_name, node_name=None, can_contain_self=False, stop_at=None):
        """
        tag_name - name of the code tag
        node_name - name of the html code tag
        """
        if stop_at == None:
            stop_at = ()
        def func(parser, token):
            if can_contain_self:
                nodelist = parser.parse(('/%s' % tag_name,) + stop_at)
            else:
                nodelist = parser.parse(('/%s' % tag_name, tag_name) + stop_at)
            name = tag_arguments(parser.tokens[0].contents)[0]
            if name == '/%s' % tag_name:
                parser.delete_first_token()
            return SimpleTagNode(token, node_name if node_name else tag_name, nodelist)
        self.tag(tag_name, func)

    def unclosed_tag(self, tag_name, node_name=None):
        def func(parser, token):
            return UnclosedTagNode(token, node_name if node_name else tag_name)
        self.tag(tag_name, func)

    def comment_tag(self, tag_name):
        def func(parser, token):
            nodelist = parser.parse(('/%s' % tag_name,))
            parser.delete_first_token()
            return CommentNode(token, tag_name, nodelist)
        self.tag(tag_name, func)

    def argumented_tag(self, tag_name, string, can_contain_self=False, stop_at=None):
        if stop_at == None:
            stop_at = ()
        def func(parser, token):
            _, arg, kargs = tag_arguments(token.contents)
            if can_contain_self:
                nodelist = parser.parse(('/%s' % tag_name,))
            else:
                nodelist = parser.parse(('/%s' % tag_name, tag_name))
            name = tag_arguments(parser.tokens[0].contents)[0]
            if name == '/%s' % tag_name:
                parser.delete_first_token()
            return ArgumentedNode(token, string, arg, kargs, nodelist)
        self.tag(tag_name, func)

    def attr_tag(self, tag_name, node_name=None, arg_name=None, attrs=None, closes=True, can_contain_self=False, stop_at=None):
        if stop_at == None:
            stop_at = ()
        def func(parser, token):
            _, arg, kargs = tag_arguments(token.contents)
            if closes:
                if can_contain_self:
                    nodelist = parser.parse(('/%s' % tag_name,) + stop_at)
                else:
                    nodelist = parser.parse(('/%s' % tag_name, tag_name) + stop_at)
                name = tag_arguments(parser.tokens[0].contents)[0]
                if name == '/%s' % tag_name:
                    parser.delete_first_token()
            else:
                nodelist = NodeList()
            return AttrNode(token, node_name if node_name else tag_name,
                    nodelist, arg_name, arg, attrs, kargs, closes)
        self.tag(tag_name, func)

    def link_tag(self, tag_name, link_arg, node_name=None, arg_name=None,
                 attrs=None, closes=True, content_attr=None):
        """
        tag_name - the name of the tag to look for
        link_arg - the attribute that conatins the link
        node_name - the name of the html element, defaults to tag_name
        arg_name - the name to give the anonymous attribute
        attrs - the name of all the allowed attributes
        closes - does the tag have a closing tag?
        content_attr - the attribute to assign the elements content to.
                closes must be false for this to be acitivated
        """
        def func(parser, token):
            _, arg, kargs = tag_arguments(token.contents)
            if closes:
                if not arg and not kargs.get(link_arg):
                    nodelist = parser.parse(('/%s' % tag_name, tag_name), collect=True)
                else:
                    nodelist = parser.parse(('/%s' % tag_name, tag_name))
                parser.delete_first_token()
            else:
                if content_attr:
                    from djangopress.core.format.parser import CHECK_NEXT
                    nodelist = parser.parse(('/%s' % tag_name, tag_name), check_first=CHECK_NEXT)
                    if nodelist:
                        parser.delete_first_token()
                        kargs[content_attr] = nodelist.contents()
                else:
                    nodelist = NodeList()
            return LinkNode(token, link_arg, node_name if node_name else tag_name,
                    nodelist, arg_name, arg, attrs, kargs, closes)
        self.tag(tag_name, func)

class Node(object):

    def __init__(self, token):
        self.token = token

    def __iter__(self):
        yield self

    def render(self, content):
        pass

    def contents(self):
        return mark_safe(self.token.contents)

    def get_nodes_by_type(self, nodetype):
        "Return a list of all nodes (within this node and its nodelist) of the given type"
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        for attr in self.child_nodelists:
            nodelist = getattr(self, attr, None)
            if nodelist:
                nodes.extend(nodelist.get_nodes_by_type(nodetype))
        return nodes

class TextNode(Node):

    def render(self, context):
        return mark_safe(self.token.contents)

class NodeList(list):
    def contents(self):
        return mark_safe(''.join(b.contents() for b in self))

    def render(self, context):
        return mark_safe(''.join(b.render(context) for b in self))

    def get_nodes_by_type(self, nodetype):
        "Return a list of all nodes of the given type"
        nodes = []
        for node in self:
            nodes.extend(node.get_nodes_by_type(nodetype))
        return nodes

class TagNode(Node):

    def contents(self):
        return "%s%s%s" % (self.token.start, self.token.contents, self.token.end)

    def render(self, context):
        return ""

    def safe_dict(self, dct):
        result = {}
        for key in dct:
            if dct[key] != None:
                result[key] = dct[key].replace('"', '&quot;')
        return result

class UnclosedTagNode(TagNode):
    def __init__(self, token, name):
        super(UnclosedTagNode, self).__init__(token)
        self.name = name

    def render(self, context):
        return "<%s />" % self.name

class AttrNode(TagNode):
    def __init__(self, token, node_name, nodelist=None, arg_name=None, arg=None, attrs=None, kargs=None, closes=True):
        super(AttrNode, self).__init__(token)
        self.node_name = node_name
        self.nodelist = nodelist
        self.arg_name = arg_name
        self.arg = arg
        self.attrs = attrs
        self.kargs = kargs
        self.closes = closes

    def _render(self, context):
        if self.attrs:
            args = dict((key, value) for key, value in self.kargs.iteritems() if key in self.attrs)
        else:
            args = {}
        if self.arg_name:
            args[self.arg_name] = self.arg
        return {
            "attrs": self.safe_dict(args),
            "tag": self.node_name,
            "content": self.nodelist.render(context) if self.nodelist else "",
            "closes": self.closes
        }

    def render(self, context):
        data = self._render(context)
        if type(data) == dict:
            return render('''<{{tag}}{% for attr, value in attrs.items %} {{attr}}="{{value}}"{% endfor %}{% if closes %}>{{ content }}</{{tag}}>{% else %} />{% endif %}''', data)
        return data

url_re = re.compile("([a-z]+)://")
url_validator = URLValidator()

class LinkNode(AttrNode):

    def __init__(self, token, link_arg, node_name, nodelist, arg_name, arg, attrs, kargs, closes):
        super(LinkNode, self).__init__(token, node_name, nodelist, arg_name, arg, attrs, kargs, closes)
        self.link_arg = link_arg

    def _render(self, context):
        if not self.kargs.get(self.link_arg) and not self.arg:
            self.arg = self.nodelist.contents()
        data = super(LinkNode, self)._render(context)
        link = data["attrs"].get(self.link_arg)
        if not link:
            return ""
        if link[0] == "#":
            return data
        if link[0] == '/':
            link = "http://%s%s" % (Site.objects.get_current(), link)
        elif self.node_name == "a":
            data["attrs"]["rel"] = "external nofollow"
        match_obj = url_re.match(link)
        if not match_obj:
            link = "http://%s" % link
        try:
            url_validator(link)
        except ValidationError:
            return data["attrs"].get(self.link_arg)
        data["attrs"][self.link_arg] = link
        return data

class ArgumentedNode(TagNode):
    def __init__(self, token, string, arg, kargs, nodelist):
        super(ArgumentedNode, self).__init__(token)
        self.arg = arg
        self.kargs = kargs
        self.nodelist = nodelist
        self.string = string

    def render(self, context):
        args = dict(self.kargs)
        args["arg"] = self.arg
        args = self.safe_dict(args)

        args['content'] = self.nodelist.render(context)
        return render(self.string, args)

class SimpleTagNode(TagNode):
    def __init__(self, token, name, nodelist):
        super(SimpleTagNode, self).__init__(token)
        self.name = name
        self.nodelist = nodelist

    def render(self, context):
        args = {
            "tag": self.name,
            "contents": self.nodelist.render(context)
        }
        return "<%(tag)s>%(contents)s</%(tag)s>" % args

class CommentNode(SimpleTagNode):

    def render(self, context):
        return ""

    def contents(self, context):
        return ""

class DefListNode(TagNode):
    def __init__(self, token, arg, items, tag):
        super(DefListNode, self).__init__(token)
        self.arg = arg
        self.items = items
        self.tag = tag

    def render(self, context):
        data = {
            "tag": self.tag,
            "items": "".join("<%s>%s</%s>" % (tag, item.render(context), tag)
                            for tag, item in self.items),
        }
        return '<%(tag)s>%(items)s</%(tag)s>' % data

def def_list_func(parser, token):
    tag, arg, _ = tag_arguments(token.contents)
    items = []
    nodelist = parser.parse(('/%s' % tag, 'dd', 'dt'))
    previous = parser.tokens[0].contents
    while previous != '/%s' % tag:
        name, _, _ = tag_arguments(parser.tokens[0].contents)
        parser.delete_first_token()
        nodelist = parser.parse(('/%s' % tag, 'dd', '/dd', 'dt', '/dt'))
        if previous[0] != "/":
            items.append((name, nodelist))
        previous = parser.tokens[0].contents
    parser.delete_first_token()
    return DefListNode(token, arg, items, tag)

class TableNode(TagNode):
    def __init__(self, token, nodelist):
        super(TableNode, self).__init__(token)
        self.nodelist = nodelist

    def render(self, context):
        return "<table>%s</table>" % (self.nodelist.render(context))

def td_func(parser, token):
    lib = Library()
    lib.attr_tag("td", attrs=("rowspan", "colspan"), stop_at=("tr",))
    lib.attr_tag("th", attrs=("rowspan", "colspan"), stop_at=("tr",))
    parser.add_library(lib)

    nodelist = parser.parse(('/tr', 'tr', "tfoot", "thead", "tbody"))

    name = tag_arguments(parser.tokens[0].contents)[0]
    if name == '/td':
        parser.delete_first_token()

    parser.pop_library()
    return SimpleTagNode(token, 'tr', nodelist)

# the col and colgroup tags are not implemented.  Support for nested tables
# is also not implemented.
def table_func(parser, token):
    lib = Library()
    lib.simple_tag("caption")
    lib.simple_tag("thead", can_contain_self=False, stop_at=("tfoot", "tbody"))
    lib.simple_tag("tfoot", can_contain_self=False, stop_at=("thead", "tbody"))
    lib.simple_tag("tbody", can_contain_self=False, stop_at=("thead", "tfoot"))
    lib.tag("tr", td_func)
    parser.add_library(lib)

    tag = tag_arguments(token.contents)[0]
    nodelist = parser.parse(('/%s' % tag,))
    parser.delete_first_token()
    # could here check that all the nodes are in the right older
    # ie, caption, thead, tfoot, tbody, and no other tags are there that should not be

    parser.pop_library()
    return TableNode(token, nodelist)