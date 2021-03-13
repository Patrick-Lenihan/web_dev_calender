DROP TABLE IF EXISTS events;

CREATE TABLE events 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    startTime INTEGER NOT NULL,
    endTime INTEGER NOT NULL,
    date TEXT NOT NULL
);
INSERT INTO events (name, startTime, endTime, date)
VALUES ('patrick', 36, 36, '2008-11-11');