from pypage._html import Tag, State


def _val_(name):
    return '{{ %s }}' % name


def _stmt_(stmt):
    return '{% ' + stmt + ' %}'


class pystmt(Tag):
    def __init__(self, stmt):
        super().__init__(stmt, html=False)


class _if_(pystmt):
    def __init__(self, cond):
        super().__init__('if ' + cond)


class _for_(pystmt):
    def __init__(self, cond):
        super().__init__('for ' + cond)

FOR = _for_
IF = _if_
VAL = _val_
STMT = _stmt_


if __name__ == '__main__':
    State.switch_gstate(State())
    with _if_('name is not None'):
        Tag('b', 'hello world')

    with _if_('True') as f:
        Tag('b', 'this is true')
        f.add(_stmt_('else'), -1)
        Tag('b', 'this is false')

    with _for_('user in names'):
        Tag('h1', 'user %s sex is %s' % (_val_('user.name'),
                                         _val_('user.sex')))

    print(State.gstate.compile())
