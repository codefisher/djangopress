
from django.template import Template, Context
from django.contrib.markup.templatetags.markup import markdown, restructuredtext, textile

from django.utils.safestring import mark_safe
from django.utils.html import urlize, escape, fix_ampersands
from djangopress.core.format.smilies import add_smilies
from djangopress.core.format.bbcode import bbcode
from djangopress.core.format.sanitized_html import sanitized_html

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
                for name, value in cls.formats.iteritems()
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

def format_plaintext(text, nofollow=True, trim_url_limit=None, smilies=True, *args, **kargs):
    return mark_safe('''<pre class="plain_text">%s</pre>'''
            % add_smilies(urlize(escape(text), nofollow=nofollow,
                trim_url_limit=trim_url_limit)), smilies=smilies)

def format_html(text, nofollow=True, trim_url_limit=None, smilies=True, *args, **kargs):
    return mark_safe(fix_ampersands(add_smilies(urlize(text,
            nofollow=nofollow, trim_url_limit=trim_url_limit), smilies=smilies)))

def format_template(text, context=None, *args, **kargs):
    t = Template(text)
    if context == None:
        context = Context()
    return mark_safe(t.render(context))

def format_markdown(text, *args, **kargs):
    return markdown(text)

def format_restructuredtext(text, *args, **kargs):
    return restructuredtext(text)

def format_textile(text, *args, **kargs):
    return textile(text)

FORMATS = {
    "markdown": {
        "function": format_markdown,
        "safe": True,
        "verbose_name": "Markdown",
    },
    "restructuredtext": {
        "function": format_restructuredtext,
        "safe": True,
        "verbose_name": "reStructuredText",
    },
    "textile": {
        "function": format_textile,
        "safe": True,
        "verbose_name": "Textile",
    },
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
        "function": sanitized_html,
        "safe": True,
        "verbose_name": "Sanitized HTML",
    },
}
for name, value in FORMATS.iteritems():
    Library.add(name, **value)

try:
    from creole import Parser
    from creole.html_emitter import HtmlEmitter
    def format_wiki(text, *args, **kargs):
        document = Parser(text).parse()
        return mark_safe(HtmlEmitter(document).emit())
    Library.add("wiki", format_wiki, True, "Wiki")
except ImportError:
    pass