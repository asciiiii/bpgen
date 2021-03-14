from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import FormField
from wtforms import SelectField
from wtforms import StringField
from wtforms import validators

from bpgen.factorio.generated.signals import SIGNALS


class CombinatorTextForm(FlaskForm):
    first_line = StringField(validators=[validators.DataRequired()], default='my text')
    second_line = StringField()


class CityBlockForm(FlaskForm):
    class CityBlockIOForm(FlaskForm):
        used = BooleanField(default=False)
        type = SelectField(choices=["item", "fluid"])
        resource = SelectField(choices=SIGNALS.keys())

    in1 = FormField(CityBlockIOForm)
    in2 = FormField(CityBlockIOForm)
    in3 = FormField(CityBlockIOForm)
    in4 = FormField(CityBlockIOForm)
    in5 = FormField(CityBlockIOForm)
    in6 = FormField(CityBlockIOForm)
    in7 = FormField(CityBlockIOForm)

    out1 = FormField(CityBlockIOForm)
    out2 = FormField(CityBlockIOForm)
    out3 = FormField(CityBlockIOForm)
    out4 = FormField(CityBlockIOForm)
    out5 = FormField(CityBlockIOForm)
    out6 = FormField(CityBlockIOForm)
    out7 = FormField(CityBlockIOForm)

    landfill = BooleanField('With landfill tiles', default=False)


class TrainForm(FlaskForm):
    type = SelectField(choices=["item", "fluid"])
    resource = SelectField(choices=SIGNALS.keys())
