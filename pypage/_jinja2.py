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


class Snippet(object):
    '''
    A reusable html snippet associated with python logic. This can make the pair of frontend and backend more modular.
    One can use it like

    class NameSnippet(Snippet):
        def __init__(self, name):
            self.name = name
            super().__init__()

        @property
        def view(self):
            Tag('h1', "my name is %s" % VAL(self.wrap_key('name))

        @property
        def logic(self):
            return {
                self.KEY('name') : 'superjomn',
            }

    and reuse this snippet anywhere for any times, and finally, in a flask application, one can render a page with
    Snippets like

    @app.route('/')
    def index():
        return
    '''
    id_prefix = "snip"
    counter = 0

    def __init__(self, id=None):
        self.id = id if id is not None else "%s__%d" % (Snippet.id_prefix,
                                                        Snippet.counter)
        Snippet.counter += 1

    @property
    def html(self):
        ''' The pypage Tags.

        For example:
            Tag('b', VAL('name'))
        '''
        raise NotImplementedError

    def logic(self):
        '''
        Parameters for this Jinja2 template snippet.
        :return: An dict for jinja2 templates.
        '''
        raise NotImplementedError

    def KEY(self, name):
        ''' Wrap a key's name to a unique id, so that the same variable name in different snippet will be unique. '''
        return "%s_%s" % (self.id, name)

    def VAL(self, name):
        return VAL(self.KEY(name))


def merge_logics(*logics):
    ''' merge dicts '''
    # check no duplicate keys
    keys = set()
    res = dict()
    for logic in logics:
        for key in logic.keys():
            assert key not in keys, "duplicate logic keys"
            keys.add(key)
        res.update(logic)
    return res


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
