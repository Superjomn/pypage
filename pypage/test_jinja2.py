from pypage._html import *
from pypage._jinja2 import Snippet, VAL


class HelloSnippet(Snippet):

    @property
    def html(self):
        Tag('h1', "my name is %s" % VAL('name'))

    @property
    def logic(self):
        return {'name': 'Superjomn'}


if __name__ == '__main__':
    snip = HelloSnippet()

    page = Page()

    with page.body:
        snip.html

    page.display(args=snip.logic())
