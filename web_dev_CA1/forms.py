from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,HiddenField, PasswordField, RadioField
from wtforms.validators import InputRequired, EqualTo

class CalenderInsertForm(FlaskForm):
    eventName = StringField("name",validators=[InputRequired(message="you must enter somthing here")]) 
    eventStart = StringField("start",validators=[InputRequired(message="you must enter somthing here")]) 
    eventEnd = StringField("end",validators=[InputRequired(message="you must enter somthing here")]) 
    date = StringField("date",validators=[InputRequired(message="you must enter somthing here")]) 
    reacuring = RadioField("does this event reacuring",
    						choices=[("No","No"),
    								("Daily","Daily"),
    								("Weekly","Weekly"),
    								("Yearly","Yearly")],
    								default="No"
    	)
    isPublic = RadioField("do you whant to make this a public event viewable to other users",
    	choices=[("No","No"),
    			("Public","Public")],
    			default="No"
    			)
    submit = SubmitField("Submit")

class HiddenFormForTodaysDate(FlaskForm):
	todaysDate = HiddenField()# found method from https://wtforms.readthedocs.io/en/2.3.x/fields/ 

class signUpForm(FlaskForm):
	name = StringField("name",validators=[InputRequired(message="you must enter somthing here")])
	username = StringField("user name",validators=[InputRequired(message="you must enter somthing here")])
	password = PasswordField("password",validators=[InputRequired(message="you must enter somthing here")])
	confirmPassword = PasswordField("confirm password",validators=[InputRequired(message="you must enter somthing here"),EqualTo('password',message="passwords must match")])
	submit = SubmitField("Submit")

class loginForm(FlaskForm):
	username = StringField("user name",validators=[InputRequired(message="you must enter somthing here")])
	password = PasswordField("password",validators=[InputRequired(message="you must enter somthing here")])
	submit = SubmitField("Submit")

class goToPublicEvent(FlaskForm):
	submit = SubmitField("Go to event")

class searchPublicEvents(FlaskForm):
	searchbar = StringField("user name",validators=[InputRequired(message="you must enter somthing here")])
	submit = SubmitField('search')

class sendMatchingRequest(FlaskForm):
	startDate = StringField('date to start search',validators=[InputRequired(message="you must enter somthing here")])
	endDate = StringField('date to end search',validators=[InputRequired(message="you must enter somthing here")])
	#startTime = StringField('earliest you can meet on each day',validators=[InputRequired(message="you must enter somthing here")])
	#endTime = StringField('Latest you can meet on each day',validators=[InputRequired(message="you must enter somthing here")])
	people = StringField('list the people you want to match you schedual with seperated by a comma',validators=[InputRequired(message="you must enter somthing here")])
	submit = SubmitField("Submit")

class HiddenFormForAcceptingMatching(FlaskForm):
	accepted = StringField()# found method from https://wtforms.readthedocs.io/en/2.3.x/fields/ 
	submit = SubmitField("accept")