import sqlite3

con = sqlite3.connect("events", check_same_thread=False)
cur = con.cursor()

def create_db():
  cur.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            event DATE NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT NOT NULL,
            posted DATE NOT NULL
        )
    ''')