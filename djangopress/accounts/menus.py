from djangopress.menus.menu import register
from django.template import Template, RequestContext
from django.core.urlresolvers import reverse

class LoginRender(object):
    def __init__(self):
        self._members = Template("""
            <li><a href="{% url 'accounts-profile' %}">Members</a>
                <ul>
                    <li><a href="{% url 'logout' %}">Logout</a></li>
                    <li><a href="{% url 'accounts-profile' %}">Profile</a></li>
                </ul></li>
        """)
        
    def render_menu(self, context, tree, menu=None):
        raise #we don't know how to do this
    
    def render_item(self, context, item, sub_menu):
        if context.get("user").is_authenticated():
            return self._members.render(RequestContext(context.get("request"), {"user": context.get("user")}))
        else:
            return """<li><a href="%s">Login</a></li>""" % reverse('login')
        
register('member', LoginRender())