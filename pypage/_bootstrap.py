from __future__ import absolute_import
__all__ = ('layout', )

from pypage._html import Tag


class layout(object):
    @staticmethod
    def container(**kwargs):
        return Tag('div', class_='container', **kwargs)

    @staticmethod
    def fluid_container(**kwargs):
        return Tag('div', class_='container-fluid', **kwargs)

    @staticmethod
    def row(**kwargs):
        return Tag('div', class_='row', **kwargs)

    @staticmethod
    def col(size=None, **kwargs):
        if size is None:
            return Tag('div', class_='col', **kwargs)
        return Tag('div', class_='col-%d' % size)

    @staticmethod
    def sm_col(**kwargs):
        return Tag('div', class_='col-sm', **kwargs)

    @staticmethod
    def colof(size):
        return Tag('div', class_='col-%d' % size)


if __name__ == '__main__':

    from _content import *
    from _components import *

    p = Page(title="hello world!")
    p.enable_bootstrap()

    with p.body:
        with layout.container():
            Tag('h1', 'PyPage Demo')
            with layout.row():
                col0 = layout.sm_col()
                col1 = layout.sm_col()
                col2 = layout.sm_col()

            with layout.row():
                with table().set_dark().set_striped() as t:
                    for row in range(3):
                        with table.row():
                            for col in range(6):
                                table.col("item%d-%d" % (row, col))
            with layout.row(style="text-align:center;"):
                img_url = 'https://upload.wikimedia.org/wikipedia/en/5/5f/Original_Doge_meme.jpg'
                img_url1 = 'https://snoozepost.com/app/uploads/2016/03/18364-doge-simplistic-doge-min-696x392.png'
                with layout.sm_col():
                    image(
                        img_url,
                        style='width:30px;').set_float_right().set_thumbnail()
                with layout.sm_col():
                    c = card()
                    c.image(src=img_url1)
                    with c.body():
                        li = list_group()
                        for i in range(5):
                            li.item('list 1')

    with col0:
        alert(c='this is column0, primary alert').set_primary()
    with col1:
        alert(c='this is column1, success alert', type='success').set_success()
    with col2:
        alert(c='this is column1, danger alert', type='danger').set_danger()

    p.display()
