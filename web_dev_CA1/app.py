from flask import Flask, render_template, redirect, url_for,g,request
from forms import CalenderInsertForm,HiddenFormForTodaysDate, signUpForm, loginForm, goToPublicEvent, searchPublicEvents,sendMatchingRequest, HiddenFormForAcceptingMatching
from database import get_db, close_db
from functions_for_calender_page import insert_event_into_db, convert_from_string_time_to_int_format, returnDB, convert_javascript_date_to_SQL_format, returnDBOnDate,time_until_client_date_change, find_day, choose_day_in_weekly_data, get_users_name
from functions_for_user_val import insert_user_into_db, check_if_username_exists
from functions_for_public_events import return_public_events, get_event, list_of_attendees, attend_public_event, user_has_not_already_attended_event, search_public_events
from functions_for_matching import store_info_about_matching,  send_matching_request, get_matching_inbox, accept_matching, return_aproved_for_matching, match_schedual, generate_matched_data_times, format_times_in_string
from validation import validate_time, validate_date, check_if_users_exit, check_if_end_before_start
from time import time
from flask import session
from flask_session import Session 
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
app = Flask(__name__)
app.config["SECRET_KEY"]="this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def load_logged_in_user():
    '''
    a function that runs before each request and gets the user name
    '''
    g.user = session.get("username",None)
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not(g.user == 'admin'):
            return redirect(url_for('login', next=url_for('admin')))
        return view(**kwargs)
    return wrapped_view

@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)#automaticly close the db after each route


@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route("/calender", methods=["GET","POST"])
@login_required
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
            #return the db
        day = find_day(hiddenForm.todaysDate.data)
        output = returnDBOnDate(day,g.user,session['client_date'],0)
        outputAdd1 = returnDBOnDate(day,g.user,session['client_date'],1)
        outputAdd2 = returnDBOnDate(day,g.user,session['client_date'],2)
        outputAdd3 = returnDBOnDate(day,g.user,session['client_date'],3)
        outputAdd4 = returnDBOnDate(day,g.user,session['client_date'],4)
        outputAdd5 = returnDBOnDate(day,g.user,session['client_date'],5)
        outputAdd6 = returnDBOnDate(day,g.user,session['client_date'],7)
        #output = returnDB()
        date_needed='False'
        users_name = get_users_name(g.user)
        return render_template('calender.html',hiddenForm=hiddenForm, output=output,outputAdd1=outputAdd1,outputAdd2=outputAdd2,outputAdd3=outputAdd3,outputAdd4=outputAdd4,outputAdd5=outputAdd5,outputAdd6=outputAdd6, date_needed=date_needed,users_name=users_name, day=day)
    return render_template('calender.html',hiddenForm=hiddenForm, output=output,date_needed=date_needed)


@app.route("/insert", methods=["GET","POST"])
@login_required
def insert():
    '''
    this is a function that is the backend of the insersion webpage
    '''
    form = CalenderInsertForm()
    #output = returnDB()
    if form.validate_on_submit():
        eventStart = form.eventStart.data
        eventStartVal = validate_time(eventStart)
        eventEnd = form.eventEnd.data
        eventEndVal = validate_time(eventEnd)
        date = form.date.data
        dateVal = validate_date(date)
        if eventStartVal == True:
            print('bang')
            if eventEndVal == True:
                print('bang!')
                if dateVal == True:
                    print('bang!!')
                    nameOfEvent = form.eventName.data
                    eventStart = convert_from_string_time_to_int_format(form.eventStart.data)
                    eventEnd = convert_from_string_time_to_int_format(form.eventEnd.data)
                    print(eventStart,eventEnd,"fksdfklj")
                    if eventEnd > eventStart:
                        reacuring = form.reacuring.data
                        reacuring = choose_day_in_weekly_data(reacuring,date)
                        isPublic = form.isPublic.data
                        insert_event_into_db(reacuring,g.user,nameOfEvent,eventStart,eventEnd,date,isPublic)
                        return render_template('success.html')
                    else:
                        form.eventEnd.errors.append("end must come after the start")
                else:
                    form.date.errors.append("not valid date")
            else:
                form.eventEnd.errors.append("not valid time")
        else:
            form.eventStart.errors.append("not valid time")
    
    return render_template('insert.html',form=form)


@app.route("/signup", methods=["GET","POST"])
def signup():
    form = signUpForm()
    if form.validate_on_submit() and check_if_username_exists(form.username.data):
        insert_user_into_db(form.username.data,form.name.data,form.password.data)
        return render_template("success.html")
    elif form.validate_on_submit() and not(check_if_username_exists(form.username.data)):
        return "already exists"
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
        if user is None:
            form.username.errors.append("Unkown user id")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("incorrect password!")
        else:
            session.clear()
            session["username"] = username
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for("calender")
            return redirect(next_page)
            #return redirect(url_for("calender"))
    return render_template("login.html",form=form)


@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET","POST"])
@admin_required
def admin():
    events = returnDB('events')
    users = returnDB('users')
    matchingRequests = returnDB('matchingRequests')
    matchingResponse = returnDB('matchingResponse')
    return render_template('admin.html',events=events,users=users,matchingResponse=matchingResponse,matchingRequests=matchingRequests)

@app.route("/public", methods=["GET","POST"])
@login_required
def public():
    form =  searchPublicEvents()
    if form.validate_on_submit():
        public_events = search_public_events(form.searchbar.data)
        return render_template('public.html',public_events=public_events,form=form)
    public_events = return_public_events()
    return render_template('public.html',public_events=public_events, form=form)

@app.route("/public_event/<int:event_id>", methods=["GET","POST"])
@login_required
def public_event(event_id):
    form = goToPublicEvent()
    event_info = get_event(event_id)
    people_attending = list_of_attendees(event_id)
    if form.validate_on_submit():
        if user_has_not_already_attended_event(people_attending,g.user):
            attend_public_event(session["username"],event_info)
        people_attending = list_of_attendees(event_id)
        return render_template("public_event.html",event_info=event_info, people_attending=people_attending,form=form)

    return render_template("public_event.html",event_info=event_info, people_attending=people_attending,form=form)


@app.route("/match", methods=["GET","POST"])
@login_required
def match():
    form = sendMatchingRequest()
    if form.validate_on_submit():
        if validate_date(form.startDate.data) == True:
            if validate_date(form.endDate.data) == True:
                if check_if_users_exit(form.people.data)== True:
                    if check_if_end_before_start(form.startDate.data,form.endDate.data):
                        table_id_num = store_info_about_matching(g.user,form.startDate.data,form.endDate.data)
                        send_matching_request(table_id_num,form.people.data)
                        return render_template("success.html")
                    else: form.endDate.errors.append("endDate must be after start date")
                else:
                    form.people.errors.append("user does not exist")
            else: form.endDate.errors.append("not valid date")
        else:
            form.startDate.errors.append("not valid date")

    return render_template("match.html",form=form)

@app.route("/inbox", methods=["GET","POST"])
@login_required
def inbox():
    form = HiddenFormForAcceptingMatching()
    if form.validate_on_submit():
        accept_matching(form.accepted.data,g.user)
    matching_requests_received = get_matching_inbox(g.user)
    data_ready_for_matching = return_aproved_for_matching(g.user)
    matched_data = match_schedual(g.user,data_ready_for_matching)
    times_free = generate_matched_data_times(matched_data)
    times_free = format_times_in_string(times_free)
    return render_template("inbox.html",matching_requests_received=matching_requests_received,form=form,data_ready_for_matching=data_ready_for_matching,times_free=times_free)