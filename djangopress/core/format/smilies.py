
def add_smilies(text, smilies=True):
    # not to self, smilies must be sourouned by space
    if not smilies:
        return text
    return text