# PyPage

PyPage is a framework that make an backend engineer develop a data driven web application easier.

It is based on Python, with Flask to offer service and bootsrap to offer a neat frontend.

# Usage
In PyPage, all the html page or Jinja2 templates are written by Python, here is a simple hello-world application

```python
from pypage import Page, layout

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
                image(img_url, style='width:30px;').set_float_right().set_thumbnail()
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
```

the above code will start a Flask service at http://127.0.0.1:8081, open it and get following page

<div align="center">
    <img src="./_images/web0.png"/>
</div>
