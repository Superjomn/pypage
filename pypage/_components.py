from _html import *
from utils import wrap_methods

@wrap_methods
class alert(Tag):
    WRAP_STYLES = (
        'primary', 'secondary', 'success', 'danger', 'warning', 'info',
        'light', 'dark'
    )
    METHOD_NAMER = lambda style: 'set_' + style

    def __init__(self, **kwargs):
        super().__init__('div', class_='alert', role='alert', **kwargs)

    def _in(self, method, style, *args, **kwargs):
        self.kwargs['class'] += ' alert-%s' % style
        return self

@wrap_methods
class badge(Tag):
    WRAP_STYLES = (
        'primary', 'secondary', 'success', 'danger', 'warning', 'info',
        'light', 'dark'
    )
    METHOD_NAMER = lambda style: 'set_' + style

    def __init__(self, **kwargs):
        super().__init__('span', class_='badge', role='alert', **kwargs)

    def _in(self, method, style, *args, **kwargs):
        self.kwargs['class'] += ' badge-%s' % style
        return self

class list_group(Tag):
    def __init__(self, **kwargs):
        super().__init__('ul', class_='list-group', **kwargs)

    def item(self, c=None, active=False, **kwargs):
        State.gstate.switch(self)
        class_ = 'list-group-item' + (' active' if active else '')
        t = Tag('li', class_=class_, c=c)
        State.gstate.switch()
        return t

class card(Tag):
    def __init__(self, **kwargs):
        super().__init__('div', class_='card')
        self._image = None
        self._body = None

    def image(self, src, **kwargs):
        if not self._image:
            State.gstate.switch(self)
            self._image = Tag('img', single=True, class_='card-img-top', src=src, **kwargs)
            State.gstate.switch()
        else:
            self._image.kwargs['src'] = src

    def body(self):
        State.gstate.switch(self)
        if not self._body:
            State.gstate.switch(self)
            self._body = Tag('div', class_='card-body')
            State.gstate.switch()
        return self._body
