def VAL(name):
    return '{{ %s }}' % name

def IF(stmt):
    return '{% %s %}' % stat


class Block(object):
    def __init__(self, stmt):
        self.content = []

    def __enter__(self):
        self.content.append
