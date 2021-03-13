from flask import Flask, render_template
from forms import CalenderInsertForm,HiddenFormForTodaysDate
from database import get_db, close_db
from functions_for_calender_page import insert_event_into_db, convert_from_string_time_to_int_format, returnDB
app = Flask(__name__)
app.config["SECRET_KEY"]="this-is-my-secret-key"

@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)#automaticly close the db after each route


@app.route("/calender", methods=["GET","POST"])
def calender():
    '''
    this is a function that is the backend of the main calender webpage
    '''
    hiddenForm = HiddenFormForTodaysDate()
    form = CalenderInsertForm()
    output = returnDB()
    if form.validate_on_submit():
        nameOfEvent = form.eventName.data
        eventStart = convert_from_string_time_to_int_format(form.eventStart.data)
        eventEnd = convert_from_string_time_to_int_format(form.eventEnd.data)
        date = form.date.data
        print(hiddenForm.todaysDate.data)
        print(len(hiddenForm.todaysDate.data))
        insert_event_into_db(nameOfEvent,eventStart,eventEnd,date)

        #return the db
        output = returnDB()
        return render_template('calender.html',hiddenForm=hiddenForm,form=form, output=output)
    
    return render_template('calender.html',hiddenForm=hiddenForm,form=form, output=output)