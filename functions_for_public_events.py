from database import get_db, close_db
def return_public_events():
	db = get_db()
	return db.execute("""SELECT * FROM events WHERE publicId IN (SELECT id FROM publicEvents)group by publicId; """)

def get_event(event_id):
	db = get_db()
	output =  db.execute("""SELECT * FROM events WHERE publicId = ? group by id; """,(event_id,)).fetchone()
	return output
def list_of_attendees(event_id):
	db = get_db()
	return db.execute("""SELECT * FROM events WHERE publicId = ?;""",(event_id,))

def attend_public_event(user_name,event_info):
	db = get_db()
	db.execute("""INSERT OR REPLACE INTO events (reacuring,user_name,name, startTime, endTime, eventDate,publicId) VALUES(?,?,?,?,?,?,?);""",(event_info['reacuring'],user_name,event_info['name'],event_info['startTime'],event_info['endTime'],event_info['eventDate'],event_info['publicId']))
	db.commit()

def user_has_not_already_attended_event(people_attending,user):
	for people in people_attending:
		if user == people['user_name']:
			return False
	return True

def search_public_events(query):
	db = get_db()
	query = '%'+query + '%'
	return db.execute("""SELECT * FROM events WHERE publicId IN (SELECT id FROM publicEvents) AND name Like ? group by publicId; """,(query,))



