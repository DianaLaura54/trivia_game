import pytest
import sqlite3
import os


@pytest.mark.database
class TestDatabaseStructure:
    def test_database_creation(self, test_db):
        conn, cursor, db_name = test_db
        assert os.path.exists(db_name)
        assert isinstance(conn, sqlite3.Connection)

    def test_test_set_table_exists(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_set'")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 'test_set'

    def test_player_table_exists(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player'")
        result = cursor.fetchone()
        assert result is not None

    def test_game_table_exists(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game'")
        result = cursor.fetchone()
        assert result is not None

    def test_question_table_exists(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='question'")
        result = cursor.fetchone()
        assert result is not None

    def test_test_table_exists(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test'")
        result = cursor.fetchone()
        assert result is not None


@pytest.mark.database
class TestDatabaseOperations:
    def test_insert_domain(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("INSERT INTO test_set (domain1) VALUES ('chemistry')")
        conn.commit()
        cursor.execute("SELECT domain1 FROM test_set WHERE domain1='chemistry'")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 'chemistry'

    def test_insert_player(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("INSERT INTO player (first_name, last_name) VALUES ('Jane', 'Smith')")
        conn.commit()
        cursor.execute("SELECT first_name, last_name FROM player WHERE first_name='Jane'")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 'Jane'
        assert result[1] == 'Smith'

    def test_insert_question(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute('''
            INSERT INTO question (question, var1, var2, var3, var4, correct)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test Question?', 'A', 'B', 'C', 'D', 'B'))
        conn.commit()
        cursor.execute("SELECT question, correct FROM question WHERE question='Test Question?'")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 'Test Question?'
        assert result[1] == 'B'

    def test_insert_game(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("SELECT idgame FROM player LIMIT 1")
        player_id = cursor.fetchone()[0]
        cursor.execute("SELECT idset FROM test_set LIMIT 1")
        set_id = cursor.fetchone()[0]
        cursor.execute('''
            INSERT INTO game (idgame, idset, date1, hour1, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_id, set_id, '2025-10-23', '14:30:00', 25))
        conn.commit()
        cursor.execute("SELECT score FROM game WHERE score=25")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 25

    def test_fetch_domains(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT domain1 FROM test_set")
        domains = cursor.fetchall()
        assert len(domains) >= 3
        assert ('informatics',) in domains
        assert ('mathematics',) in domains


@pytest.mark.database
class TestDatabaseQueries:
    def test_fetch_questions_by_domain(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT q.question, q.correct
            FROM question q
            JOIN test t ON q.idint = t.idint
            JOIN test_set ts ON ts.idset = t.idset
            WHERE ts.domain1 = ?
        ''', ('informatics',))
        questions = cursor.fetchall()
        assert len(questions) > 0
        assert all(len(q) == 2 for q in questions)

    def test_fetch_player_scores(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT p.first_name, p.last_name, g.score
            FROM player p
            JOIN game g ON p.idgame = g.idgame
        ''')
        results = cursor.fetchall()
        assert len(results) > 0
        assert results[0][0] == 'John'
        assert results[0][1] == 'Doe'
        assert results[0][2] == 15

    def test_fetch_top_scorer(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("INSERT INTO player (first_name, last_name) VALUES ('Alice', 'Wonder')")
        alice_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO game (idgame, idset, date1, hour1, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (alice_id, 1, '2025-10-23', '15:00:00', 50))
        conn.commit()
        cursor.execute('''
            SELECT p.first_name, p.last_name, g.score
            FROM player p
            JOIN game g ON p.idgame = g.idgame
            WHERE g.score = (SELECT MAX(score) FROM game)
        ''')
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 'Alice'
        assert result[2] == 50

    def test_count_players(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("SELECT COUNT(*) FROM player")
        count = cursor.fetchone()[0]
        assert count >= 1

    def test_fetch_players_by_domain(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT DISTINCT p.first_name, p.last_name
            FROM player p
            JOIN game g ON p.idgame = g.idgame
            JOIN test_set ts ON g.idset = ts.idset
            WHERE ts.domain1 = ?
        ''', ('informatics',))
        players = cursor.fetchall()
        assert len(players) > 0


@pytest.mark.database
class TestDataIntegrity:
    def test_question_has_all_fields(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("SELECT * FROM question LIMIT 1")
        question = cursor.fetchone()
        assert len(question) == 7  # idint, question, var1, var2, var3, var4, correct

    def test_foreign_key_relationship(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT g.idgame, p.idgame
            FROM game g
            JOIN player p ON g.idgame = p.idgame
        ''')
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == result[1]

    def test_domain_uniqueness(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT COUNT(DISTINCT domain1) FROM test_set")
        count = cursor.fetchone()[0]
        assert count >= 3