from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators

from bpgen.factorio.blueprint import Blueprint
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

    in_count = StringField('In count', [validators.DataRequired()])
    out_count = StringField('Out count', [validators.DataRequired()])
    submit = SubmitField('Generate')
