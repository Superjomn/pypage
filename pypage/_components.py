from pypage._html import *
from pypage.utils import wrap_methods


def navbar(logotxt, links, link_txts, active=None, theme='light', color='light'):
    '''
    logotxt: a setence as logo.
    links: list of string.
    link_txts: list of string.
    active: the active link's setence.
    '''
    navbar_class = "navbar-%s" % theme
    navbar_color = None
    style = None
    if color in ('primary', 'dark'):
        tag = Tag(
            'nav',
            class_='navbar navbar-expand-lg %s bg-%s' % (navbar_class, color))
    else:
        tag = Tag(
            'nav',
            class_='navbar navbar-expand-lg %s' % navbar_class,
            style="background-color:%s" % color)

    with tag:
        Tag('a', logotxt, class_='navbar-brand', href='/')

        with Tag('div', class_='collapse navbar-collapse', id='navbarNav'):
            with Tag('ul', class_='navbar-nav'):
                for idx,link in enumerate(links):
                    with Tag('li', class_='nav-item'):
                        Tag('a', link_txts[idx], class_='nav-link', href='%s' % link)


@wrap_methods
class alert(Tag):
    WRAP_STYLES = ('primary', 'secondary', 'success', 'danger', 'warning',
                   'info', 'light', 'dark')
    METHOD_NAMER = lambda style: 'set_' + style

    def __init__(self, c=None, **kwargs):
        super().__init__('div', c=c, class_='alert', role='alert', **kwargs)

    def _in(self, method, style, *args, **kwargs):
        self.kwargs['class'] += ' alert-%s' % style
        return self


@wrap_methods
class badge(Tag):
    WRAP_STYLES = ('primary', 'secondary', 'success', 'danger', 'warning',
                   'info', 'light', 'dark')
    METHOD_NAMER = lambda style: 'set_' + style

    def __init__(self, c=None, **kwargs):
        super().__init__('span', c=c, class_='badge', role='alert', **kwargs)

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
            self._image = Tag(
                'img', single=True, class_='card-img-top', src=src, **kwargs)
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
