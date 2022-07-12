import sqlite3 as sq

def sqlStart ():
    global base, cur
    base = sq.connect('personal.db')
    cur = base.cursor()
    if base:
        print('Data base connected.')

        base.execute('''CREATE TABLE IF NOT EXISTS trainings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, 
            user_id INTEGER,
            priority TEXT,
            rest INTEGER,
            last REAL
            )''')

        base.execute('''CREATE TABLE IF NOT EXISTS exercises(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, 
            user_id INTEGER,
            type TEXT,
            weight TEXT,
            sets TEXT,
            rest INTEGER,
            last REAL
            )''')

        base.execute('''CREATE TABLE IF NOT EXISTS trainings_consist(
            training_id INTEGER,
            exercise_id INTEGER
            )''')

        base.execute('''CREATE TABLE IF NOT EXISTS days(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            train_date REAL, 
            result TEXT
            )''')

    base.commit()