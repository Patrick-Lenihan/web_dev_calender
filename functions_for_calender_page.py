from database import get_db, close_db
def insert_event_into_db(nameOfEvent,eventStart,eventEnd,eventDate):
    '''
    this is a function that inserts an event into the database 
    '''
    db = get_db()
    db.execute("""INSERT INTO events (name, startTime, endTime, eventDate) VALUES(?,?,?,?);""",(nameOfEvent,eventStart,eventEnd,eventDate))
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

def convert_javascript_date_to_SQL_format(date):
    '''
    converting javascript date from client into YYYY-MM-DD format for storage in sqlite
    '''
    months = {"Jan":'01', "Feb":'02', "Mar":'03', "Apr":'04', "May":'05', "Jun":'06', "Jul":'07', "Aug":'08', "Sep":'09', "Oct":'10', "Nov":'11', "Dec":'12'}
    date = date.split(" ")
    return date[3]+"-"+months[date[1]]+'-'+date[2]

def time_until_client_date_change(date):
    '''
    this is a function that records the number of hours away a date is from changing
    '''
    date = date.split(" ")
    client_time = date[4]
    client_time = client_time.split(":")
    return 24 - int(client_time[0])

def returnDBOnDate(eventDate,offset):
    '''
    this is a fuction that returns the database for display but only on a specific date
    in the format YYYY-MM-DD
    '''
    offset_string = "+"+str(offset)+" day"
    db = get_db()
    return db.execute("""SELECT * FROM events WHERE eventDate = date(?,?) ORDER BY startTime;""",(eventDate,offset_string)).fetchall()
