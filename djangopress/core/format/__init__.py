from django.template import Template, Context
#from django.contrib.markup.templatetags.markup import markdown, restructuredtext, textile

from django.utils.safestring import mark_safe
from django.utils.html import urlize, escape
from djangopress.core.format.smilies import add_smilies
from djangopress.core.format.bbcode import bbcode
from djangopress.core.format.sanitized_html import sanitized_html
from djangopress.core.format import magic_html as magic_html_mod
from djangopress.core.format import html
from django.utils.encoding import force_unicode

class Library(object):
    formats = {}

    @classmethod
    def add(cls, name, function, safe=True, verbose_name=None):
        if not verbose_name:
            verbose_name = name
        cls.formats[name] = {
            "function": function,
            "safe": safe,
            "name": verbose_name
        }
        

    @classmethod
    def choices(cls, safe=True):
        return [(name, value["name"])
                for name, value in cls.formats.items()
            if value["safe"] or not safe]

    @classmethod
    def get(cls, name, safe=True):
        format = cls.formats.get(name)
        if format and (format["safe"] or not safe):
            return format
        raise ValueError("format %s not supported" % name)

    @classmethod
    def format(cls, name, text, safe=True, *args, **kargs):
        format = cls.formats.get(name)
        if format and (format["safe"] or not safe):
            return format["function"](text, *args, **kargs)
        raise ValueError("format %s not supported" % name)

def format_plaintext(text, nofollow=True, trim_url_limit=None, smilies=True, should_urlize=True, *args, **kargs):
    if should_urlize:
        urlize(escape(text), nofollow=nofollow, trim_url_limit=trim_url_limit)
    else:
        text = escape(text)
    return mark_safe(force_unicode('''<pre class="plain_text">%s</pre>'''
            % add_smilies(text, smilies=smilies),
                encoding='utf-8'))

def format_html(text, nofollow=True, trim_url_limit=None, smilies=True, *args, **kargs):
    return mark_safe(force_unicode(text, encoding='utf-8'))
    #return mark_safe(force_unicode(fix_ampersands(add_smilies(urlize(text,
    #        nofollow=nofollow, trim_url_limit=trim_url_limit), smilies=smilies)),
    #        encoding='utf-8'))

def format_template(text, context=None, *args, **kargs):
    t = Template(text)
    if context == None:
        context = Context()
    return mark_safe(force_unicode(t.render(context), encoding='utf-8'))

FORMATS = {
    "plain_text": {
        "function": format_plaintext,
        "safe": True,
        "verbose_name": "Plain Text",
    },
    "template": {
        "function": format_template,
        "safe": False,
        "verbose_name": "Django Template",
    },
    "html": {
        "function": format_html,
        "safe": False,
        "verbose_name": "HTML",
    },
    "bbcode": {
        "function": bbcode,
        "safe": True,
        "verbose_name": "BBcode",
    },
    "sanitized_html": {
        "function": html.sanatized_html,
        "safe": True,
        "verbose_name": "Sanitized HTML",
    },
    "magic_html": {
        "function": magic_html_mod.magic_html,
        "safe": False,
        "verbose_name": "Magic HTML",
    },
    "extended_html": {
        "function": html.extended_html,
        "safe": False,
        "verbose_name": "Extended HTML",
    },
}
for name, value in FORMATS.items():
    Library.add(name, **value)

try:
    from creole import Parser
    from creole.html_emitter import HtmlEmitter
    def format_wiki(text, *args, **kargs):
        document = Parser(text).parse()
        return mark_safe(force_unicode(HtmlEmitter(document).emit(),
                 encoding='utf-8', output='utf-8'))
    Library.add("wiki", format_wiki, True, "Wiki")
except ImportError:
    pass

try:
    # added to make it fail if not installed, but we still use the
    # the Django function because it is easier
    import textile
    def format_textile(text, *args, **kargs):
        return mark_safe(textile(text))
    Library.add("textile", format_textile, True, "Textile")
except ImportError:
    pass

try:
    import markdown
    import bleach
    def format_markdown(text, *args, **kargs):
        return mark_safe(markdown.markdown(bleach.clean(text)))
    Library.add("markdown", format_markdown, True, "Markdown")
except ImportError:
    pass

try:
    from restructed_text import html_body
    def format_restructuredtext(text, *args, **kargs):
        return mark_safe(html_body(text))
    Library.add("restructuredtext", format_restructuredtext, True, "reStructuredText")
except ImportError:
    pass