import os
import sys
import html

from flask import Flask, render_template

INDENT = '    '


def repr_(s):
    s = repr(s)
    return '"' + s[1:-1] + '"'


class State(object):
    gstate = None

    def __init__(self):
        self.main_queue = []
        self.indent = 0
        self.stack = [self.main_queue]
        self.instances = set()

    def switch(self, tag=None):
        if tag:
            self.stack.append(tag.content)
        else:
            self.stack.pop()

    @staticmethod
    def switch_gstate(state):
        State.gstate = state

    def append(self, content):
        '''
        one Tag instance might be appended multiple times, that's OK.
        It will be removed in compile.
        '''
        if isinstance(content, Tag) and content in self.instances:
            return

        last = self.stack[-1]
        last.append(content)
        self.instances.add(content)

    def compile(self):
        return compile(self.main_queue)

    def clear(self):
        self.main_queue.clear()
        indent = 0
        self.stack = [self.main_queue]


class Tag(object):
    def __init__(self, name_, c=None, html=True, single=False, **kwargs):
        self.name = name_
        self.kwargs = kwargs
        self.html = html
        self.content = []
        self.pre = None
        self.single = single
        if 'class_' in kwargs:
            class_ = kwargs["class_"]
            del self.kwargs['class_']
            self.kwargs['class'] = class_
        self._top_indent = State.gstate.indent

        self.__enter__()
        if c is not None:
            self.add(c)
        self.__exit__(None, None, None)

    def as_row(self):
        self.kwargs.setdefault('class', '')
        self.kwargs['class'] += ' row'
        return self

    def as_col(self, size=None):
        self.kwargs.setdefault('class', '')
        if size is not None:
            assert isinstance(size, int)
            self.kwargs['class'] += ' col-%d' % size
        else:
            self.kwargs['class'] += ' col'
        return self

    def as_container(self):
        self.kwargs.setdefault('class', '')
        self.kwargs['class'] += ' container'
        return self

    def as_container_fluid(self):
        self.kwargs.setdefault('class', '')
        self.kwargs['class'] += ' container-fluid'
        return self

    def __enter__(self):
        if self not in State.gstate.instances:
            State.gstate.append(self)
        State.gstate.switch(self)
        State.gstate.indent = self._top_indent
        State.gstate.indent += 1
        return self

    def __exit__(self, type, value, traceback):
        State.gstate.indent -= 1
        State.gstate.switch()

    def __str__(self):
        indent = self._top_indent * INDENT
        if not self.single:
            self._start_tag = self._html_block_start(
            ) if self.html else self._jinja_block_start()
            self._end_tag = self._html_block_end(
            ) if self.html else self._jinja_block_end()
            self.content.insert(0, indent + self._start_tag)
            self.content.append(indent + self._end_tag)
            return compile(self.content)
        else:
            return indent + '<{name} {attrs}/>'.format(
                name=self.name, attrs=self._attrs)

    def add(self, c, offset=0):
        indent = INDENT * (self._top_indent + 1 + offset)
        State.gstate.append(indent + c)

    def _html_block_start(self):
        if isinstance(self.name, list):
            assert not self.kwargs
            return ''.join(["<%s>" % n for n in self.name])
        return '<{name}{attrs}>'.format(
            name=self.name,
            attrs=self._attrs,
        )

    def _html_block_end(self):
        if isinstance(self.name, list):
            return ''.join(["</%s>" % n for n in reversed(self.name)])
        return '</%s>' % self.name

    def _jinja_block_start(self):
        return '{% ' + self.name + ' %}'

    def _jinja_block_end(self):
        return '{% ' + 'end%s' % self.name.split()[0] + ' %}'

    @property
    def _attrs(self):
        return ' '.join([
            " %s=%s" % (key, repr_(value))
            for key, value in self.kwargs.items()
        ])

    def __repr__(self):
        return self.__str__()


class RawHtml(object):
    def __init__(self, txt):
        State.gstate.append(txt)


class Style(Tag):
    def __init__(self, **kwargs):
        super().__init__('style')

    def add(self, idcls, attr_values):
        '''
        cls: id or cls
        attr_va
        '''
        State.gstate.append('%s {' % idcls)
        for (attr, value) in attr_values:
            State.gstate.append('%s:%s;' % (attr, value))


def page_switch_gstate(f):
    def handler(*args, **kwargs):
        self = args[0]
        State.switch_gstate(self.state)
        return f(*args, **kwargs)

    return handler


class Page(Tag):
    '''
    include a <html>
    '''

    def __init__(self, title="", filename="tmp.html", debug=False):
        self.state = State()
        self.filename = filename
        self.debug = debug
        State.switch_gstate(self.state)
        super().__init__('html')
        self._title = title
        with self:
            self._style = Style()
            self._body = Tag('body', style='margin:0px;padding:0px;')

    @page_switch_gstate
    def set_title(self, title):
        self._title = title

    @property
    def body(self):
        State.switch_gstate(self.state)
        return self._body

    @property
    def style(self):
        State.switch_gstate(self.state)
        return self._style

    def compile(self, tpl_dir='template'):
        path = os.path.join(tpl_dir, self.filename)
        with open(path, 'w') as f:
            f.write(self.state.compile())

    @page_switch_gstate
    def compile_str(self):
        source = self.state.compile()
        if self.debug:
            RawHtml('<hr/>')
            Tag('h3', 'template source code')
            RawHtml('<pre><code>%s</code></pre>' % html.escape(source))

        return source

    def display(self, host='0.0.0.0', port=8081, tpl_dir='template', args={}):
        ''' start a flask service and display this page. '''
        SERVER_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
        STATIC_DIR = os.path.join(SERVER_PATH, tpl_dir)
        if not os.path.isdir(tpl_dir):
            os.mkdir(tpl_dir)
        with open(os.path.join(tpl_dir, self.filename), 'w') as f:
            f.write(self.state.compile())
        print('server root', SERVER_PATH)
        print('static dir', STATIC_DIR)

        app = Flask(
            __name__, static_url_path=STATIC_DIR, template_folder=STATIC_DIR)
        #app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

        @app.route('/')
        def display():
            return render_template(self.filename, **args)

        app.run(debug=True, host=host, port=port)

    @page_switch_gstate
    def enable_bootstrap(self):
        with self:
            RawHtml(
                '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'
            )
            RawHtml(
                '<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>'
            )
            RawHtml(
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>'
            )
            RawHtml(
                '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>'
            )
        return self

    @page_switch_gstate
    def enable_echarts(self):
        ''' Add pyecharts scripts '''
        host = "https://pyecharts.github.io/assets/js"
        with self._body:
            RawHtml('\n'.join([
                '{% for jsfile_name in script_list %}',
                '<script src="%s/{{ jsfile_name }}.js"></script>' % host,
                '{% endfor %}',
            ]))
        return self

def compile(li):
    '''
    li: a list

    compile and skip duplicate items.
    '''
    compiled = set()
    lines = []
    for item in li:
        if isinstance(item, Tag):
            if item not in compiled:
                c = str(item)
                lines.append(c)
                compiled.add(item)
        else:
            lines.append(str(item))

    return '\n'.join(lines)


if __name__ == '__main__':
    page = Page(title='hello world')
    page.enable_bootstrap()
    with page.body:
        Tag('h1', c='hello world')
    # page.display()

    page1 = Page(title='another page')
    page1.enable_bootstrap()
    with page1.body:
        Tag('h1', c='hello world, superjomn')
        Tag('h2', c='there are many fruits')
    page1.display()
