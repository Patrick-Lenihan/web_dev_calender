from database import get_db, close_db
def create_table_for_storing_matching_users(user,startDate,endDate,startTime,endTime,people):
	db = get_db()
	inset = str(user)+"MatchTable"
	db.execute("""CREATE TABLE IF NOT EXISTS? (
		tableName TEXT NOT NULL PRIMARY KEY,
		user TEXT NOT NULL,
		startDate TEXT NOT NULL,
		endDate TEXT NOT NULL,
		startTime TEXT NOT NULL,
		endTime TEXT NOT NULL);""",(inset,))
	
	returndb = db.execute("""SELECT * FROM ?  """,(insert,))
	returndb = insert+str(len(returndb))
	db.execute("""INSERT INTO ? (tableName,user,startDate,endDate,startTime,endTime) VALUES(?,?,?,?,?,?); """,(inset,returndb,startDate,endDate,startTime,endTime))
	db.execute("""CREATE TABLE ? (
				user_name TEXT NOT NULL,
				agreed BOOLEAN NOT NULL
		);""",(returndb))
	return returndb
	db.commit()