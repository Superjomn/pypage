import unittest
from html import gstate, Tag, Page

class TestTag(unittest.TestCase):
    def setUp(self):
        gstate.clear()

    def test_html_block_start(self):
        Tag('b', c='hello', font='somefont', class_='someclass')
        c = gstate.compile()
        print(c)



class TestHTML(unittest.TestCase):
    def setUp(self):
        gstate.clear()

    def test_main(self):
        with Tag('b', class_='some_class'):
            Tag('span', c='hello world', font='somefont')

        c = gstate.compile()
        print(c)
        self.assertEqual(c, '''<b class='some_class'>
    <span font='somefont'>
        hello world
    </span>
</b>''')

    def test_page(self):
        page = Page()
        with page.body:
            Tag('p', 'hello world')
        with page.body:
            Tag('b', 'some other content')
        c = gstate.compile()
        print('body test')
        print(c)

if __name__ == '__main__':
    unittest.main()
