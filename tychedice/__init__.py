#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import the stuffs!

"""`main` is the top level module for this application."""

from flask import Flask, render_template, request
from flask.ext.assets import Environment, Bundle

import datetime
import json
import re
import traceback

def create_app(config_location='config.BaseConfiguration'):
    app = Flask(__name__)
    app.config.from_object(config_location)
    return app

app = create_app()

#########################################################################
# Using JS and CSS bundlers to minify code.
assets = Environment(app)

js = Bundle(
    'js/*.js',
#    filters='jsmin',
    output='gen/jspacked.js'
)
assets.register('js_all', js)

css = Bundle('css/*.css',
#    filters='yui_css',
#    output='gen/csspacked.css'
)
assets.register('css_all', css)

#########################################################################

@app.route('/')
def indexpage():
  return render_template('home.html')
 
if __name__ == '__main__':
    app = create_app
    app.run()
