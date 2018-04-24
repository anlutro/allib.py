#!/usr/bin/env python

from allib.web import Application

app = Application('testapp', debug=True)
app.add_route('GET', '/', lambda req: 'hello world')
app.run('127.0.0.1', 8000)
