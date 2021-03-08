#!bin/python

import os

from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

from bpgen.forms import CityBlockForm
from bpgen.forms import CombinatorTextForm

DEBUG = False
BLUEPRINT_PREVIEW_URL = 'https://fbe.teoxoy.com/?source='

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=os.urandom(32))
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def main():
    tabs = [
        CombinatorTextForm(request.form),
        CityBlockForm(request.form),
    ]

    if request.method == 'POST':
        for tab in tabs:
            if not tab.submit.data:
                continue

            if not tab.validate_on_submit():
                continue

            result = tab.generate()
            tab.result = {
                'blueprint': result,
                'preview_url': BLUEPRINT_PREVIEW_URL + result,
            }

    return render_template('main.html', title="ascii's blueprint generator", tabs=tabs)


if __name__ == '__main__':
    args = {}

    if DEBUG:
        args['debug'] = DEBUG
    else:
        args['host'] = '0.0.0.0'

    app.run(**args)
