from djangopress.menus.menu import register
from django.template import Template, RequestContext
from django.urls import reverse

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
            if context.get("request").path == reverse('logout'):
                return Template("""<li><a href="{% url 'login' %}?next={{ request.path }}">Login</a></li>""").render(context)
            return Template("""<li><a href="{% url 'login' %}">Login</a></li>""").render(context)
        
register('member', LoginRender())