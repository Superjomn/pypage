import functools
from _html import Tag
from utils import wrap_methods


@wrap_methods
class table(Tag):
    WRAP_STYLES = ('table-dark', 'table-striped', 'table-sm', 'table-hover')

    def METHOD_NAMER(style): return 'set_' + '_'.join(style.split('-')[1:])

    class row(Tag):
        def __init__(self, c=None, **kwargs):
            super().__init__('tr', **kwargs)
            if c is not None:
                assert isinstance(c, list)
                with self:
                    for col in c:
                        Tag('td', c=str(col))

    class col(Tag):
        def __init__(self, c=None, **kwargs):
            super().__init__('td', c=c, **kwargs)

    def __init__(self, **kwargs):
        super().__init__('table', class_='table', **kwargs)

    def _in(self, method, style, *args, **kwargs):
        self.kwargs['class'] += ' %s' % style
        return self


@wrap_methods
class image(Tag):
    WRAP_STYLES = (
        'img-fluid',
        'img-thumbnail',
        'float-left',
        'float-right',
        'rounded')

    def METHOD_NAMER(style): return 'set_' + '_'.join(style.split('-')[1:])

    def __init__(self, src, **kwargs):
        super().__init__('img', single=True, src=src, class_='img-fluid')

    def _in(self, method, style, *args, **kwargs):
        self.kwargs['class'] += ' %s' % style
        return self

    @staticmethod
    def METHOD_NAMER(style):
        fs = style.split('-')
        if style.startswith('img-'):
            fs = fs[1:]
        return 'set_%s' % '_'.join(fs)


class code(Tag):
    def __init__(self, **kwargs):
        super().__init__(name=['pre', 'code'])
