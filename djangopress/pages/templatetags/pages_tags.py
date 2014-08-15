from django import template
from django.template.loader import render_to_string
from djangopress.pages.blocks import PageBlock
register = template.Library()

def do_placeholder(parser, token):
    args = token.split_contents()
    nodelist = None
    if len(args) < 2:
        raise template.TemplateSyntaxError, "not enough arguments"
    if "with_default" in args:
        nodelist = parser.parse(('endplaceholder',))
        parser.delete_first_token()
    name = args[1][1:-1]
    return PlaceholderNode(name, nodelist, identifier="identifier" in args)

class PlaceholderNode(template.Node):
    def __init__(self, name, nodelist=None, identifier=False):
        self.nodelist = nodelist
        self._name = name
        self._identifier = identifier

    def get_placeholder_name(self):
        return self._name

    def render(self, context):
        user = context.get('user')
        page = context.get('page')
        if self._identifier:
            blocks = PageBlock.objects.filter(block_id=self._name)
        else:
            blocks = page.blocks.filter(block_name=self._name)
        content = "\n".join(block.content(context) for block in blocks)
        if not content and self.nodelist:
            content = self.nodelist.render(context)
        if (context.get('enable_page_edit') and user
                and user.has_perm('pages.change_page')):
            data = {
                "blocks": blocks,
                "page": page,
                "name": self._name,
                "content": content,
                "identifier": self._identifier,
            }
            return render_to_string("pages/editor/page_block.html", data, context_instance=context)
        else:
            return content

register.tag('placeholder', do_placeholder)
