#!bin/python
import argparse
import glob
import os
import pathlib
import shutil

from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect

from bpgen.factorio.blueprint import Blueprint
from bpgen.factorio.cityblock import CityBlock
from bpgen.factorio.cityblock import replace_item
from bpgen.factorio.entity import generate_combinator_text
from bpgen.forms import CityBlockForm
from bpgen.forms import CombinatorTextForm
from bpgen.forms import TrainForm

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
    return redirect("/cityblock", code=302)


@app.route('/train')
def train():
    form = TrainForm(request.args)

    template_args = {
        'form': form,
    }

    if request.args and form.validate():
        blueprint = CityBlock('train')

        type_ = 'item' if form.type.data.lower() == 'solid' else 'fluid'

        if form.type.data.lower() == 'liquid':
            for entity in blueprint.data['blueprint']['entities']:
                entity = replace_item(entity, 'name', {'cargo-wagon': 'fluid-wagon'})

        for station in blueprint.data['blueprint']['schedules'][0]['schedule']:
            if station['station'] == '[item=iron-ore]OUT':
                station['station'] = '[{}={}] OUT'.format(type_, form.resource.data)
            elif station['station'] == '[item=iron-ore]IN':
                station['station'] = '[{}={}] IN'.format(type_, form.resource.data)

        template_args['result'] = build_result(blueprint)

    return render_template('autoform.html', **template_args)


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

    return render_template('autoform.html', **template_args)


def cccc(blueprint, form, out, pos):
    if not form.used.data:
        return

    station = CityBlock('station_{}_{}'.format('out' if out else 'in', form.type.data.lower()))
    type_ = 'item' if form.type.data.lower() == 'solid' else 'fluid'
    station.data['blueprint'] = replace_item(station.data['blueprint'], 'name', {'wood': form.resource.data})

    if form.type.data.lower() == 'liquid':
        for entity in station.data['blueprint']['entities']:
            entity = replace_item(entity, 'type', {'item': 'fluid'})

    station.data['blueprint'] = replace_item(station.data['blueprint'], 'station', {'[item=wood] IN': '[{}={}] IN'.format(type_, form.resource.data)})
    station.data['blueprint'] = replace_item(station.data['blueprint'], 'station', {'[item=wood] OUT': '[{}={}] OUT'.format(type_, form.resource.data)})
    blueprint.add_entities(station.data['blueprint']['entities'], pos, out)


@app.route('/cityblock')
def cityblock():
    form = CityBlockForm(request.args)

    template_args = {
        'form': form,
    }

    if request.args and form.validate():
        blueprint = CityBlock('cityblock')

        cccc(blueprint, form.in1.form, False, 1)
        cccc(blueprint, form.in2.form, False, 2)
        cccc(blueprint, form.in3.form, False, 3)
        cccc(blueprint, form.in4.form, False, 4)
        cccc(blueprint, form.in5.form, False, 5)
        cccc(blueprint, form.in6.form, False, 6)
        cccc(blueprint, form.in7.form, False, 7)

        cccc(blueprint, form.out1.form, True, 1)
        cccc(blueprint, form.out2.form, True, 2)
        cccc(blueprint, form.out3.form, True, 3)
        cccc(blueprint, form.out4.form, True, 4)
        cccc(blueprint, form.out5.form, True, 5)
        cccc(blueprint, form.out6.form, True, 6)
        cccc(blueprint, form.out7.form, True, 7)

        if form.landfill.data:
            blueprint.add_landfill()

        template_args['result'] = build_result(blueprint)

    return render_template('cityblock.html', **template_args)


def move_exported_blueprints():
    path = os.path.expanduser('~/.factorio/script-output/')

    dst = pathlib.Path(__file__).parent.absolute()
    dst = os.path.join(dst, 'blueprints')

    for file in glob.glob(path + '*.blueprint'):
        print(file, dst)
        shutil.copy(file, dst)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--debug", action="store_true")
    args = arg_parser.parse_args()

    flask_args = {}

    if args.debug:
        flask_args['debug'] = True
        move_exported_blueprints()
    else:
        flask_args['host'] = '0.0.0.0'

    app.run(**flask_args)
