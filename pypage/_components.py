from pypage._html import *
from pypage.utils import wrap_methods
from pyecharts import Line


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


class collapse:
    count = 0
    def __init__(self):
        self._btn = None
        self._trg = None
        self._trg_id = "collapse-%d" % collapse.count
        collapse.count += 1

    @property
    def btn(self):
        if self._btn is None:
            extra = {'data-toggle': 'collapse',
                     'aria-expanded': 'false',
                     'aria-controls': self._trg_id}
            self._btn = Tag('a', class_='btn btn-primary',
                            href='#%s' % self._trg_id,
                            role='button',
                            **extra)
        return self._btn

    @property
    def trg(self):
        if self._trg is None:
            with Tag('div', class_='collapse', id=self._trg_id):
                with Tag('div', class_='card card-body') as _:
                    self._trg = _
        return self._trg


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


def scalar(title, x, y, mark_point=['min', 'max']):
    '''
    title: str
    x: list of strs
    y: list of number
    '''
    line = Line(title)
    line.add('line', x, y, mark_point)
    return line.render_embed(), line.get_js_dependencies()
