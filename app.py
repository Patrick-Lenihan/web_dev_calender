from flask import Flask, render_template
from forms import CalenderInsertForm
from database import get_db, close_db
app = Flask(__name__)
app.config["SECRET_KEY"]="this-is-my-secret-key"

@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)#automaticly close the db after each route

def insert_event_into_db(nameOfEvent,eventStart,eventEnd,date):
    '''
    this is a function that inserts an event into the database 
    '''
    db = get_db()
    db.execute("""INSERT INTO events (name, startTime, endTime, date) VALUES(?,?,?,?);""",(nameOfEvent,eventStart,eventEnd,date))
    db.commit()


def convert_from_string_time_to_int_format(stime):
    '''
    tis is a function that converts the time in the format HH:MM to plan MM sutable for the db
    '''
    stime = stime.split(':')
    for i in range(2):
        stime[i] = int(stime[i])
    stime[0] = stime[0]*60
    return stime[0]+stime[1]


def returnDB():
    '''
    this is a fuction that returns the database for display
    '''
    db = get_db()
    return db.execute("""SELECT * FROM events ORDER BY startTime;""").fetchall()


@app.route("/calender", methods=["GET","POST"])
def calender():
    '''
    this is a function that is the backend of the main calender webpage
    '''
    form = CalenderInsertForm()
    output = returnDB()
    if form.validate_on_submit():
        nameOfEvent = form.eventName.data
        eventStart = convert_from_string_time_to_int_format(form.eventStart.data)
        eventEnd = convert_from_string_time_to_int_format(form.eventEnd.data)
        date = form.date.data
        insert_event_into_db(nameOfEvent,eventStart,eventEnd,date)

        #return the db
        output = returnDB()
        return render_template('calender.html',form=form, output=output)
    
    return render_template('calender.html',form=form, output=output)