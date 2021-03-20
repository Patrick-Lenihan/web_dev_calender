from database import get_db
from werkzeug.security import generate_password_hash

def insert_user_into_db(username,name,password):
    '''
    this is a function that inserts a user into the database and stores there password as a hash 
    '''
    db = get_db()
    db.execute("""INSERT INTO users (user_name,name,password) VALUES(?,?,?);""",(username,name,generate_password_hash(password)))
    db.commit()
