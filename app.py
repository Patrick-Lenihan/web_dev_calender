from flask import Flask, render_template
from forms import CalenderInsertForm,HiddenFormForTodaysDate
from database import get_db, close_db
from functions_for_calender_page import insert_event_into_db, convert_from_string_time_to_int_format, returnDB, convert_javascript_date_to_SQL_format, returnDBOnDate
from flask import session
from flask_session import Session 
app = Flask(__name__)
app.config["SECRET_KEY"]="this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)#automaticly close the db after each route

@app.route("/calender", methods=["GET","POST"])
def calender():
    hiddenForm = HiddenFormForTodaysDate()
    output = ""
    date_needed = 'True'
    if hiddenForm.validate_on_submit():
        if "client_date" not in session:
            session["client_date"]= convert_javascript_date_to_SQL_format(hiddenForm.todaysDate.data)
            #return the db
        output = returnDBOnDate(session['client_date'])
        #output = returnDB()
        date_needed='False'
        return render_template('calender.html',hiddenForm=hiddenForm, output=output, date_needed=date_needed)
    return render_template('calender.html',hiddenForm=hiddenForm, output=output,date_needed=date_needed)


@app.route("/insert", methods=["GET","POST"])
def insert():
    '''
    this is a function that is the backend of the insersion webpage
    '''
    form = CalenderInsertForm()
    output = returnDB()
    if form.validate_on_submit():
        nameOfEvent = form.eventName.data
        eventStart = convert_from_string_time_to_int_format(form.eventStart.data)
        eventEnd = convert_from_string_time_to_int_format(form.eventEnd.data)
        date = form.date.data
        insert_event_into_db(nameOfEvent,eventStart,eventEnd,date)
        return render_template('insert.html',form=form)
    
    return render_template('insert.html',form=form)