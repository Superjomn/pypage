# PyPage

PyPage is a framework that make an backend engineer develop a data driven web application easier.

It is based on Python, with Flask to offer service and bootsrap to offer a neat frontend.

# Usage
In PyPage, all the html page or Jinja2 templates are written by Python, here is a simple hello-world application

```python
import pypage as p2
from pypage import Page

p = Page(id="page0", title="hello world!")

with p.row():
    p2.h1('hello world!')
```

The Jinja2 template is supported natively

```python
import pypage as p2
from pypage import Page
from pypage.jinja2 import VAL, FOR, IF

p = Page(id="page0", title="hello world!")
# equal to p.id('page0'); p.title('hello world')

with p2.table(header=["name", "sex", "age"]):
    with FOR('rcd in records'):
        with p2.row() as x:
            x.add(VAL('rcd.name'))
            x.add(VAL('rcd.sex))
            x.add(VAL('rcd.age))
            # equal to p2.row(VAL('rcd.name'), VAL('rcd.sex'), VAL('rcd.age'))
```
