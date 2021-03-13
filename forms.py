from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,HiddenField
from wtforms.validators import InputRequired

class CalenderInsertForm(FlaskForm):
    eventName = StringField("name",validators=[InputRequired(message="you must enter somthing here")]) 
    eventStart = StringField("start",validators=[InputRequired(message="you must enter somthing here")]) 
    eventEnd = StringField("end",validators=[InputRequired(message="you must enter somthing here")]) 
    date = StringField("date",validators=[InputRequired(message="you must enter somthing here")]) 
    submit = SubmitField("Submit")

class HiddenFormForTodaysDate(FlaskForm):
	todaysDate = HiddenField()# found method from https://wtforms.readthedocs.io/en/2.3.x/fields/ 
