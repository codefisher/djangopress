from django import template
register = template.Library()

def do_placeholder(parser, token):
    args = token.split_contents()
    nodelist = None
    if len(args) < 2:
        raise template.TemplateSyntaxError, "not enough arguments"
    if len(args) == 3:
        if args[2] == "with_default":
            nodelist = parser.parse(('endplaceholder',))
        else:
            raise template.TemplateSyntaxError, "invalid 2nd argument"
    name = args[1][1:-1]
    return PlaceholderNode(name, nodelist)

class PlaceholderNode(template.Node):
    def __init__(self, name, nodelist=None):
        self.nodelist = nodelist
        self.name = name

    def get_placeholder_name(self):
        return self.name

    def render(self, context):
        blocks = context.get('page').blocks
        output = "\n".join(block.content(context) for block in blocks.filter(block_name=self.name))
        if not output and self.nodelist:
            output = self.nodelist.render(context)
        return output

register.tag('placeholder', do_placeholder)