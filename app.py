from flask import Flask, render_template, redirect, url_for
from forms import CalenderInsertForm,HiddenFormForTodaysDate, signUpForm, loginForm
from database import get_db, close_db
from functions_for_calender_page import insert_event_into_db, convert_from_string_time_to_int_format, returnDB, convert_javascript_date_to_SQL_format, returnDBOnDate,time_until_client_date_change
from functions_for_user_val import insert_user_into_db
from time import time
from flask import session
from flask_session import Session 
from werkzeug.security import check_password_hash, generate_password_hash
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
    unix_time = (int(time()))//60 
    hiddenForm = HiddenFormForTodaysDate()
    output = ""

    date_needed = 'True'
    if hiddenForm.validate_on_submit():
        if ("client_date" not in session) or (session['time_until_change'] < (unix_time-session['server_date'])):
            session["time_until_change"] = time_until_client_date_change(hiddenForm.todaysDate.data)
            session["client_date"]= convert_javascript_date_to_SQL_format(hiddenForm.todaysDate.data)
            session["server_date"] = unix_time #recording the time in hours since 1 Jan 1970 for 
            print(session['time_until_change'])
            #return the db
        output = returnDBOnDate(session['client_date'],0)
        outputAdd1 = returnDBOnDate(session['client_date'],1)
        outputAdd2 = returnDBOnDate(session['client_date'],2)
        outputAdd3 = returnDBOnDate(session['client_date'],3)
        outputAdd4 = returnDBOnDate(session['client_date'],4)
        outputAdd5 = returnDBOnDate(session['client_date'],5)
        outputAdd6 = returnDBOnDate(session['client_date'],6)
        #output = returnDB()
        date_needed='False'
        return render_template('calender_test.html',hiddenForm=hiddenForm, output=output,outputAdd1=outputAdd1,outputAdd2=outputAdd2,outputAdd3=outputAdd3,outputAdd4=outputAdd4,outputAdd5=outputAdd5,outputAdd6=outputAdd6, date_needed=date_needed)
    return render_template('calender_test.html',hiddenForm=hiddenForm, output=output,date_needed=date_needed)


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


@app.route("/signup", methods=["GET","POST"])
def signup():
    form = signUpForm()
    if form.validate_on_submit():
        insert_user_into_db(form.username.data,form.name.data,form.password.data)
    return render_template('signup.html',form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        db = get_db()
        user = db.execute("""SELECT * FROM users 
            WHERE user_name = ?;""", (username,)).fetchone()
        print(generate_password_hash("k"))
        print(user['password'])
        if user is None:
            print("hi")
            form.username.errors.append("Unkown user id")
        elif not check_password_hash(user["password"], password):
            print("howdy")
            form.password.errors.append("incorrect password!")
        else:
            session.clear()
            print("hello")
            session["username"] = username
            return redirect(url_for("calender"))
    return render_template("login.html",form=form)

