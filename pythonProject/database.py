import sqlite3


def extract_data():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    return conn, cursor

def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_set (
            idset INTEGER PRIMARY KEY AUTOINCREMENT,
            domain1 TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            idgame INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game (
            idgame INTEGER,
            idset INTEGER,
            date1 TEXT,
            hour1 TEXT,
            score INTEGER,
            FOREIGN KEY (idset) REFERENCES test_set (idset),
            FOREIGN KEY (idgame) REFERENCES player (idgame)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            idint INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            var1 TEXT NOT NULL,
            var2 TEXT NOT NULL,
            var3 TEXT NOT NULL,
            var4 TEXT NOT NULL,
            correct TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test (
            idset INTEGER,
            idint INTEGER,
            FOREIGN KEY (idset) REFERENCES test_set (idset),
            FOREIGN KEY (idint) REFERENCES question (idint)
        )
    ''')

def transform_data(cursor):
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('informatics')")
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('mathematics')")
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('physics')")
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('biology')")
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('chemistry')")
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('general')")

def load_data(cursor, conn):
    conn.commit()
    cursor.close()
    conn.close()


conn, cursor = extract_data()
create_tables(cursor)
transform_data(cursor)
load_data(cursor, conn)

print("Tables created successfully, domains inserted into test_set, and database initialized!")
