from bootstrap import *
from html import Status
import unittest


with Tag('html'):
    with layout.container():
        with layout.row():
            with layout.sm_col():
                components.badge(c="hello world")
            with layout.sm_col():
                Tag('b', c='this is a bold')

        with layout.row():
            Tag('h1', c='this is a head')

print(Status.compile())
