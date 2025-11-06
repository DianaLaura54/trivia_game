import pytest
import sqlite3
import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def test_db():
    test_db_name = 'test_database.db'
    if os.path.exists(test_db_name):
        os.remove(test_db_name)
    conn = sqlite3.connect(test_db_name) #database connected
    cursor = conn.cursor() #cursor


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
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('informatics')")
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('mathematics')")
    cursor.execute("INSERT INTO test_set (domain1) VALUES ('physics')")
    conn.commit() #commit the changes to the database
    yield conn, cursor, test_db_name
    cursor.close()
    conn.close()
    if os.path.exists(test_db_name):
        os.remove(test_db_name)


@pytest.fixture
def sample_questions():
    return [
        ('What is 2 + 2?', '4', ['3', '4', '5', '6']),
        ('What is the capital of France?', 'Paris', ['London', 'Berlin', 'Paris', 'Rome']),
        ('What does CPU stand for?', 'Central Processing Unit',
         ['Computer Processing Unit', 'Central Processing Unit', 'Central Program Unit', 'Core Processing Unit'])
    ]


@pytest.fixture
def populated_test_db(test_db, sample_questions):
    conn, cursor, db_name = test_db
    for idx, (question, correct, options) in enumerate(sample_questions, 1):
        cursor.execute('''
            INSERT INTO question (idint, question, var1, var2, var3, var4, correct)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (idx, question, options[0], options[1], options[2], options[3], correct))


        cursor.execute('INSERT INTO test (idset, idint) VALUES (?, ?)', (1, idx))

    cursor.execute("INSERT INTO player (first_name, last_name) VALUES ('John', 'Doe')")
    player_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO game (idgame, idset, date1, hour1, score)
        VALUES (?, ?, ?, ?, ?)
    ''', (player_id, 1, '2025-10-23', '10:00:00', 15))
    conn.commit()

    return conn, cursor, db_name