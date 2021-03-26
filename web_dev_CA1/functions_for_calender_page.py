from database import get_db, close_db
from datetime import date
from datetime import datetime,timedelta
def insert_event_into_db(reacuring,username,nameOfEvent,eventStart,eventEnd,eventDate,isPublic):
    '''
    this is a function that inserts an event into the database 
    '''
    db = get_db()
    db.execute("""INSERT INTO events (reacuring,user_name,name, startTime, endTime, eventDate,publicId) VALUES(?,?,?,?,?,?,?);""",(reacuring,username,nameOfEvent,eventStart,eventEnd,eventDate,isPublic))
    if isPublic == "Public":
        db.execute("""INSERT INTO publicEvents (last_edit) VALUES(?);""",("yes",))
        db.execute("""UPDATE events 
            SET publicId = (Select id from publicEvents WHERE last_edit = 'yes')
            WHERE publicId = 'Public';""")
        db.execute("""UPDATE publicEvents SET last_edit = 'None' """)
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


def returnDB(table):
    '''
    this is a fuction that returns the database for display
    '''
    db = get_db()
    query ='SELECT * FROM '+table +' ;'
    return db.execute(query).fetchall()

def convert_javascript_date_to_SQL_format(jdate):
    '''
    converting javascript date from client into YYYY-MM-DD format for storage in sqlite
    '''
    months = {"Jan":'01', "Feb":'02', "Mar":'03', "Apr":'04', "May":'05', "Jun":'06', "Jul":'07', "Aug":'08', "Sep":'09', "Oct":'10', "Nov":'11', "Dec":'12'}
    jdate = jdate.split(" ")
    return jdate[3]+"-"+months[jdate[1]]+'-'+jdate[2]

def time_until_client_date_change(jdate):
    '''
    this is a function that records the number of hours away a date is from changing
    '''
    jdate = jdate.split(" ")
    client_time = jdate[4]
    client_time = client_time.split(":")
    return 24 - int(client_time[0])

def returnDBOnDate(day,username,eventDate,offset):
    '''
    this is a fuction that returns the database for display but only on a specific date
    in the format YYYY-MM-DD
    '''
    num_to_dates = ['0','1','2','3','4','5','6','0','1','2','3','4','5','6']
    day = num_to_dates[day+offset]
    offset_string = "+"+str(offset)+" day"
    db = get_db()
    half_date = date.fromisoformat(eventDate)+timedelta(days=offset)
    half_date = half_date.isoformat()
    half_date = half_date.split("-")
    half_date = half_date[1]+'-'+half_date[2]
    return db.execute("""SELECT * FROM events WHERE ((eventDate = date(?,?))or (reacuring = 'Daily')or (reacuring=?)or(reacuring=? ))AND user_name = ? ORDER BY startTime;""",(eventDate,offset_string,day,half_date,username)).fetchall()

def find_day(javascript_date):
    '''
    this function takes in a javascript date and turrns it into a numeric value to be used in place of a day
    '''
    javascript_date = javascript_date.split(" ")
    dates_to_nums = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
    return dates_to_nums[javascript_date[0]]

def choose_day_in_weekly_data(reacuring,event_date):
    '''
    gets of the week from a date
    '''
    if reacuring == "Weekly":
        # fucntions found at https://docs.python.org/3/library/datetime.html
        event_date = date.fromisoformat(event_date)
        day = event_date.weekday()
        return day
    elif reacuring == "Yearly":
        half_date = event_date.split("-")
        half_date = half_date[1]+'-'+half_date[2]
        return half_date
    return reacuring

def get_users_name(user_name):
    db = get_db()
    users_name = db.execute("""SELECT name FROM users WHERE user_name = ?;""",(user_name,)).fetchone()
    return users_name['name']






