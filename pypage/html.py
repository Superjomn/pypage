class Status:
    main_queue = []
    cur = main_queue
    indent = 0

    @staticmethod
    def switch(queue=None):
        Status.cur = queue if queue is not None else Status.main_queue

    @staticmethod
    def append(content):
        Status.cur.append(content)

    @staticmethod
    def compile():
        return '\n'.join(str(_) for _ in Status.cur)


INDENT_LEN = 4


class Tag(object):
    def __init__(self, name, html=True, c=None, **kwargs):
        self.name = name
        self.kwargs = kwargs
        self.html = html
        self.content = []
        if 'class_' in kwargs:
            class_ = kwargs["class_"]
            del self.kwargs['class_']
            self.kwargs['class'] = class_
        if c is not None:
            self.__enter__()
            self.__exit__(None, None, None)

    def __enter__(self):
        Status.append(self)
        Status.switch(self.content)
        tag = self._html_block_start(
        ) if self.html else self._jinja_block_start()
        self.content.append(self.indent_placeholder + tag)
        Status.indent += 1

    def __exit__(self, type, value, traceback):
        Status.indent -= 1
        tag = self._html_block_end() if self.html else self._jinja_block_end()
        self.content.append(self.indent_placeholder + tag)
        Status.switch()

    def __str__(self):
        return '\n'.join(str(_) for _ in self.content)

    @property
    def indent_placeholder(self):
        return ' ' * INDENT_LEN * Status.indent

    def _html_block_start(self):
        if isinstance(self.name, list):
            assert not self.kwargs
            return ''.join(["<%s>" % n for n in self.name])
        return '<{name}{attrs}>'.format(
            name=self.name,
            attrs=' '.join([
                " %s=%s" % (key, repr(value))
                for key, value in self.kwargs.items()
            ]))

    def _html_block_end(self):
        if isinstance(self.name, list):
            return ''.join(["</%s>" % n for n in reversed(self.name)])
        return '</%s>' % self.name

    def _jinja_block_start(self):
        return '{%' + self.name + '%}'

    def _jinja_block_end(self):
        return '{%' + 'end%s' % self.name.split()[0] + '%}'

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    with Tag('div', class_='class0'):
        Tag('b', c="hello world")

    print(Status.compile())
