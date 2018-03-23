from .html import Status, Tag


class table(Tag):
    class row(Tag):
        def __init__(self, c=None, **kwargs):
            super().__init__(self, 'tr', **kwargs)
            if c is not None:
                assert isinstance(c, list)
                with self:
                    for col in c:
                        Tag('td', c=str(col))

    class col(Tag):
        def __init__(self, c=None, **kwargs):
            super().__init__(self, 'td', c=c, **kwargs)

    def __init__(self, **kwargs):
        super().__init__(self, 'table', class_='table', **kwargs)


class code(Tag):
    def __init__(self, **kwargs):
        super().__init__(self, name=['pre', 'code'])


class layout(object):
    @staticmethod
    def container():
        return Tag('div', class_='container')

    @staticmethod
    def row():
        return Tag('div', class_='row')

    @staticmethod
    def sm_col():
        return Tag('div', class_='col-sm')

    @staticmethod
    def colof(size):
        return Tag('div', class_='col-%d' % size)


class components(object):
    types = {
        'primary', 'secondary', 'success', 'danger', 'warning', 'info',
        'light', 'dark'
    }

    @staticmethod
    def alert(type='primary', c=None):
        assert type in components.types
        return Tag('div', c=c, class_='alert alert-%s' % type, role="alert")

    @staticmethod
    def badge(type='primary', c=None):
        assert type in components.types
        return Tag('span', c=c, class_='badge badge-%s' % type)

    class list_group(Tag):
        def __init__(self, **kwargs):
            super().__init__(self, 'ul', class_='list-group', **kwargs)

        def item(self, c=None, active=False, **kwargs):
            class_ = 'list-group-item' + 'active' if active else ''
            return Tag('li', class_=class_, c=c)
