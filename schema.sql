DROP TABLE IF EXISTS publicEvents;

CREATE TABLE publicEvents 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_edit TEXT
    );
    /*
DROP TABLE IF EXISTS events;

CREATE TABLE events 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reacuring Text NOT NULL,
    user_name TEXT NOT NULL,
    name TEXT NOT NULL,
    startTime INTEGER NOT NULL,
    endTime INTEGER NOT NULL,
    eventDate TEXT NOT NULL,
    publicId INTEGER
);
INSERT INTO events (reacuring,user_name,name, startTime, endTime, Eventdate)
VALUES ('No','r','patrick', 36, 36, '2008-11-11');*/
/*DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    name TEXT NOT NULL,
    user_name TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL
);
INSERT INTO users (user_name,name,password)
VALUES ('paddy','pad','power');*/