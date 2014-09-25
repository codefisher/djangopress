from django.conf import settings
import re

smiles_info = [
    ("emoticon-smile", [':-)', ':)', ':D', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)']),
    ("emoticon-unhappy", ['>:[', ':-(', ':(', ':-c', ':c', ':-<', ':<', ':-[', ':[', ':{']),
    ("emoticon-unhappy-wink", [";("]),
    ("emoticon-cry", [":'-(", ":'("]),
    ("emoticon-wink", [';-)', ';)', '*-)', '*)', ';-]', ';]', ';D', ';^)', ':-, ']),
    ("emoticon-tongue", ['>:P', ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', 'd:']),
    ("emoticon-surprise", ['>:O', ':-O', ':O', ':-o', ':o', '8-0', 'O_O', 'o-o', 'O_o', 'o_O', 'o_o', 'O-O']),
    ("emoticon-no-expression", [':|', ':-|']),
]



smiles_re = []
for name, values in smiles_info:
    smiles_re.append((name, re.compile(r'(^|\s)(%s)(\s|$)' % '|'.join([re.escape(i) for i in values]))))

def add_smilies(text, smilies=True):
    if not smilies:
        return text
    for name, regexp in smiles_re:
        text = regexp.sub(r' <img alt="\2" src="%s%s.png"> ' % (settings.SMILIES_ICON_FOLDER, name), text)
    return text