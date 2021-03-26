from database import get_db, close_db
from datetime import date
from datetime import datetime,timedelta
def store_info_about_matching(user,start_date,end_date):
	db = get_db()
	db.execute("""INSERT INTO matchingRequests (user,startDate,endDate,last_edit) VALUES(?,?,?,?);""",(user,start_date,end_date,'1'))
	output = db.execute(""" SELECT id FROM matchingRequests WHERE last_edit = '1' """).fetchone()
	db.execute(""" UPDATE matchingRequests SET last_edit = '0' WHERE id = ? ;""",(output[0],))
	db.commit()
	return output[0]

def send_matching_request(for_id,people):
 	db = get_db()
 	people = people.split(",")
 	for person in people:
 		db.execute("""INSERT INTO matchingResponse (user_name,for_id,accepted) VALUES (?,?,?);""",(person,for_id,'0'))

 	db.commit()

def get_matching_inbox(user):
	db = get_db()
	return db.execute(""" SELECT * FROM matchingRequests WHERE id IN (SELECT for_id FROM matchingResponse WHERE (user_name = ?)AND(accepted= "0")); """,(user,))

def accept_matching(event_id, user):
	db = get_db()
	db.execute(""" UPDATE matchingResponse SET accepted = '1' WHERE ((for_id = ?)AND(user_name = ?));""",(event_id,user))
	db.commit()

def return_aproved_for_matching(user):
	db = get_db()
	list_of_users_requests = db.execute("""SELECT * FROM matchingResponse WHERE (for_id IN (SELECT id FROM matchingRequests WHERE user = ?))""",(user,)).fetchall()
	unfinished_requests = []
	finished_requests = []
	for row in list_of_users_requests:
		if row['accepted'] == '0':
			unfinished_requests.append(row['for_id'])
	for request in list_of_users_requests:
		if not(request['for_id'] in unfinished_requests):
			finished_requests.append(request['for_id'])
	finished_requests = set(finished_requests)
	return list(finished_requests)

def match_schedual(user,groups_to_match):
	db = get_db()
	output_list = []
	for group in groups_to_match:
		matching_info = db.execute("""SELECT * FROM matchingRequests WHERE id = ?;""",(group,)).fetchone()
		users_to_match = db.execute("""SELECT id, user_name FROM matchingResponse WHERE for_id = ? Union SELECT id, user as user_name FROM matchingRequests WHERE id = ?;""",(group,group)).fetchall()
		end_date = date.fromisoformat(matching_info['endDate'])
		start_date = date.fromisoformat(matching_info['startDate'])
		if start_date != end_date:
			number_of_days = abs(end_date-start_date)# abs function found in python docs at https://docs.python.org/3/library/datetime.html#examples-of-usage-date
			number_of_days = str(number_of_days)
			number_of_days = number_of_days.split(",")
			number_of_days = number_of_days[0].split(" ")
			number_of_days = int(number_of_days[0])
		else:
			number_of_days = 0
		preliminery_ouput_list = []
		preliminery_ouput_list.append(group)
		for day in range(0,number_of_days+1):
			# get date 
			today = start_date+timedelta(days=day)
			today = today.isoformat()
			# make list of minits 
			day_list = []
			for minit in range(1441):
				day_list.append(minit)
			for user in users_to_match:
				# list all the events user has on that day
				events = db.execute("""SELECT * FROM events WHERE (user_name = ?)AND (eventDate = ?)""",(user['user_name'],today))
				# insert them into the dictionary
				for event in events:
					for i in range(int(event['startTime']),int(event['endTime'])+1):
						if i in day_list:
							day_list.remove(i)
			preliminery_ouput_list.append(day_list)
		output_list.append(preliminery_ouput_list)
	return output_list

def generate_matched_data_times(list_of_times):
	output_list = []
	for group in list_of_times:
		for k in range(1,len(group)):
			list_of_ranges = []
			list_of_ranges.append(group[0])
			start = 0
			for time in range(0,len(group[k])-1):
				if not((group[k][time+1] - group[k][time]) == 1):
					list_of_ranges.append(start)
					list_of_ranges.append(group[k][time])
					start = group[k][time+1]
				elif time == len(group[k])-2:
					list_of_ranges.append(start)
					list_of_ranges.append(group[k][time])
			output_list.append(list_of_ranges)
	return output_list

def int_to_string_time(int_input):
	return str(int_input//60)+":"+str(int_input%60)

def format_times_in_string(times):
	print(times)
	output = []
	for group in times:
		temp_list = [group[0]]
		for i in range(1,len(group)-1):
			if i%2== 1:
				temp_list.append(int_to_string_time(group[i])+"-"+int_to_string_time(group[i+1]))
		output.append(temp_list)
	print(output)
	return(output)












