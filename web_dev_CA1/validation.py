from database import get_db, close_db
from datetime import date
def validate_time(time):
	'''
	preforms validation for the time checks if : is there checks everything but the : is a number and on.....
	'''
	numbers = ['0','1','2','3','4','5','6','7','8','9']
	isColon = False
	for char in time:
		if char == ':':
			isColon = True
	if isColon == False:
		return False
	time = time.split(':')
	if not(0 < len(time) < 3):
		return False
	for i,part in enumerate(time):
		for char in part:
			if not(char in numbers):
				return False
		if i == 0 and 24 < int(part):
			return False
		elif i == 1 and 60 < int(part):
			return False
	return True

def validate_date(date):
	'''
	verefys that the date pressented is a valid date
	'''
	numbers = ['0','1','2','3','4','5','6','7','8','9']
	isDash = 0
	for char in date:
		if char == '-':
			isDash += 1
	if not(isDash == 2):
		return False
	date = date.split("-")
	for i,part in enumerate(date):
		for char in part:
			if not(char in numbers):
				return False
		if i == 1 and not(0<int(part)<13):
			return False
		elif i == 2 and not(0<int(part)<32):
			return False
	return True

def check_if_users_exit(users):
	db = get_db()
	users = users.split(',')
	for user in users:
		search = db.execute("""SELECT * from users where user_name = ?;""",(user,)).fetchone()
		if search == None:
			return False
	return True

def check_if_end_before_start(start,end):
	if date.fromisoformat(start)>date.fromisoformat(end):
		return False
	return True