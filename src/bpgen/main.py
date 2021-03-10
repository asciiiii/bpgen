#!bin/python

from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect

from bpgen.factorio.blueprint import Blueprint
from bpgen.factorio.cityblock import CityBlock
from bpgen.factorio.entity import generate_combinator_text
from bpgen.forms import CityBlockForm
from bpgen.forms import CombinatorTextForm

DEBUG = True
BLUEPRINT_PREVIEW_URL = 'https://fbe.teoxoy.com/?source='

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
bootstrap = Bootstrap(app)


def build_result(blueprint):
    encoded = blueprint.get_encoded()
    return {
        'blueprint': encoded,
        'preview_url': BLUEPRINT_PREVIEW_URL + encoded,
    }


@app.route('/')
def start():
    return redirect("/combtext", code=302)


@app.route('/combtext')
def combtext():
    form = CombinatorTextForm(request.args)

    template_args = {
        'form': form,
    }

    if request.args and form.validate():
        blueprint = Blueprint()
        entities = generate_combinator_text(form.first_line.data, form.second_line.data)
        blueprint.entities.extend(entities)
        template_args['result'] = build_result(blueprint)

    return render_template('combtext.html', **template_args)


@app.route('/cityblock')
def cityblock():
    form = CityBlockForm(request.args)

    template_args = {
        'form': form,
    }

    if request.args and form.validate():
        blueprint = CityBlock('cityblock')

        if form.landfill.data:
            blueprint.add_landfill()

        template_args['result'] = build_result(blueprint)

    return render_template('cityblock.html', **template_args)


if __name__ == '__main__':
    args = {}

    if DEBUG:
        args['debug'] = DEBUG
    else:
        args['host'] = '0.0.0.0'

    app.run(**args)
