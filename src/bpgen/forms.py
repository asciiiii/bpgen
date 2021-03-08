from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators

from bpgen.factorio.blueprint import Blueprint
from bpgen.factorio.cityblock import CityBlock
from bpgen.factorio.entity import generate_combinator_text


class Tab(FlaskForm):
    def generate(self):
        raise NotImplementedError


class CombinatorTextForm(Tab):
    tab_name = "Combinator text"
    tab_id = "combinatortext"

    first_line = StringField('First line', [validators.DataRequired()], default='my cool text')
    second_line = StringField('Second line')
    submit = SubmitField('Generate')

    def generate(self):
        bp = Blueprint()
        entities = generate_combinator_text(self.first_line.data, self.second_line.data)
        bp.entities.extend(entities)
        return bp.get_encoded()


class CityBlockForm(Tab):
    tab_name = "City block"
    tab_id = "cityblock"

    in_count = IntegerField('In count', [validators.DataRequired()], default=1)
    out_count = IntegerField('Out count', [validators.DataRequired()], default=1)
    landfill = BooleanField('With landfill tiles (preview and copy buttons not working)', default=False)
    submit = SubmitField('Generate')

    def generate(self):
        cb = CityBlock('factorio/cityblock.json')

        if self.landfill.data:
            cb.add_landfill()

        return cb.get_encoded()
