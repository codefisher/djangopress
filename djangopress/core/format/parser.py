import re
from djangopress.core.format.nodes import NodeList, TagNode, TextNode, tag_name_re, Library

"""
Written while looking at the Django template code.  There is a large
amount of coping going on.
"""

TOKEN_TAG = 0
TOKEN_TEXT = 1

class Token(object):
    def __init__(self, token_type, contents, start=None, end=None):
        self.token_type = token_type
        self.start = start
        self.end = end
        self.contents = contents
        self.lineno = None

    def __repr__(self):
        return "%s %r:%s" % (self.token_type, self.contents, self.lineno)

class Lexer(object):

    TAG_START = '['
    TAG_END = ']'
    tag_re = re.compile('(%s.*?%s)' % (re.escape(TAG_START), re.escape(TAG_END)), re.DOTALL)

    def __init__(self, template_string):
        self.template_string = template_string
        self.lineno = 1

    def tokenize(self):
        "Return a list of tokens from a given block of text."
        in_tag = False
        result = []
        for bit in self.tag_re.split(self.template_string):
            if bit:
                result.append(self.create_token(bit, in_tag))
            in_tag = not in_tag
        return result

    def create_token(self, token_string, in_tag):
        if in_tag:
            contents = token_string[len(self.TAG_START):-len(self.TAG_END)]
            token = Token(TOKEN_TAG, contents, self.TAG_START, self.TAG_END)
        else:
            token = Token(TOKEN_TEXT, token_string)
        token.lineno = self.lineno
        self.lineno += token_string.count('\n')
        return token

CHECK_NONE = 0
CHECK_ALL = 1
CHECK_NEXT = 2

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.tags = Library()

    def parse(self, parse_until=None, collect=False, check_first=CHECK_NONE):
        if parse_until is None: parse_until = []
        nodelist = self.create_nodelist()
        if parse_until and check_first:
            for token in self.tokens:
                if token.token_type == TOKEN_TAG and check_first == CHECK_NEXT:
                    if token.contents.lower() in parse_until:
                        break
                    else:
                        return nodelist
                if (token.token_type == TOKEN_TAG
                        and token.contents.lower() in parse_until):
                    break
            else:
                return nodelist
        while self.tokens:
            token = self.next_token()
            if token.token_type == TOKEN_TEXT:
                self.create_text(nodelist, token)
            elif token.token_type == TOKEN_TAG:
                if token.contents.lower() in parse_until:
                    # put token back on token list so calling code knows why it terminated
                    self.prepend_token(token)
                    return nodelist
                elif collect:
                    self.parse_error(nodelist, token)
                    continue
                try:
                    command = tag_name_re.split(token.contents, 1)[0].lower()
                except IndexError:
                    self.parse_error(nodelist, token)
                    continue
                try:
                    compile_func = self.tags.get(command)
                except KeyError:
                    self.parse_error(nodelist, token)
                    continue
                #try:
                compiled_result = compile_func(self, token)
                #except:
                #    self.parse_error(nodelist, token)
                #    continue
                self.extend_nodelist(nodelist, compiled_result)
        if parse_until:
            self.unclosed_tag(parse_until)
        return nodelist

    def create_text(self, nodelist, token):
        self.extend_nodelist(nodelist, TextNode(token))

    def parse_error(self, nodelist, token):
        self.extend_nodelist(nodelist, TagNode(token))

    def unclosed_tag(self, tags):
        self.tokens.append(Token(TOKEN_TAG, tags[0]))

    def skip_past(self, endtag):
        while self.tokens:
            token = self.next_token()
            if token.token_type == TOKEN_TAG and token.contents == endtag:
                return
        self.unclosed_tag([endtag])

    def create_nodelist(self):
        return NodeList()

    def extend_nodelist(self, nodelist, node):
        nodelist.append(node)

    def next_token(self):
        return self.tokens.pop(0)

    def delete_first_token(self):
        del self.tokens[0]

    def prepend_token(self, token):
        self.tokens.insert(0, token)

def encode_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')