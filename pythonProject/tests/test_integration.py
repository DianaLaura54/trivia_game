import pytest
import sqlite3
import os
import sys
TEST_DB = 'test_database.db'


@pytest.mark.integration
class TestQuestionFetching:
    def test_fetch_questions_returns_list(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT q.question, q.var1, q.var2, q.var3, q.var4, q.correct
            FROM question q
            JOIN test t ON q.idint = t.idint
            JOIN test_set ts ON ts.idset = t.idset
            WHERE ts.domain1 = ?
        ''', ('informatics',))
        questions = cursor.fetchall()
        assert isinstance(questions, list)
        assert len(questions) > 0

    def test_question_structure(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT q.question, q.var1, q.var2, q.var3, q.var4, q.correct
            FROM question q
            JOIN test t ON q.idint = t.idint
            JOIN test_set ts ON ts.idset = t.idset
            WHERE ts.domain1 = ?
            LIMIT 1
        ''', ('informatics',))

        question = cursor.fetchone()
        assert len(question) == 6
        assert isinstance(question[0], str)
        assert isinstance(question[5], str)

    def test_fetch_questions_for_invalid_category(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT q.question, q.var1, q.var2, q.var3, q.var4, q.correct
            FROM question q
            JOIN test t ON q.idint = t.idint
            JOIN test_set ts ON ts.idset = t.idset
            WHERE ts.domain1 = ?
        ''', ('nonexistent_category',))
        questions = cursor.fetchall()
        assert len(questions) == 0


@pytest.mark.integration
class TestScoreCalculation:
    def test_initial_score_is_zero(self):
        score = 0
        assert score == 0

    def test_score_increment_on_correct_answer(self):
        score = 0
        correct_answer = 'Paris'
        user_answer = 'Paris'

        if user_answer == correct_answer:
            score += 5

        assert score == 5

    def test_score_no_change_on_wrong_answer(self):
        score = 10
        correct_answer = 'Paris'
        user_answer = 'London'

        if user_answer == correct_answer:
            score += 5

        assert score == 10

    def test_multiple_correct_answers(self):
        score = 0
        questions_and_answers = [
            ('Paris', 'Paris'),
            ('4', '4'),
            ('CPU', 'CPU')
        ]

        for correct, user in questions_and_answers:
            if user == correct:
                score += 5

        assert score == 15

    def test_save_score_to_database(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("SELECT idgame FROM player WHERE first_name='John' AND last_name='Doe'")
        player_id = cursor.fetchone()[0]
        cursor.execute('''
            INSERT INTO game (idgame, idset, date1, hour1, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_id, 1, '2025-10-23', '16:00:00', 45))
        conn.commit()
        cursor.execute("SELECT score FROM game WHERE score=45")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 45


@pytest.mark.integration
class TestPlayerManagement:
    def test_create_new_player(self, test_db):
        conn, cursor, db_name = test_db
        first_name = 'Test'
        last_name = 'Player'
        cursor.execute('''
            INSERT INTO player (first_name, last_name) VALUES (?, ?)
        ''', (first_name, last_name))
        conn.commit()
        cursor.execute('''
            SELECT first_name, last_name FROM player 
            WHERE first_name=? AND last_name=?
        ''', (first_name, last_name))
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == first_name
        assert result[1] == last_name

    def test_retrieve_player_id(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT idgame FROM player WHERE first_name=? AND last_name=?
        ''', ('John', 'Doe'))
        player = cursor.fetchone()
        assert player is not None
        assert isinstance(player[0], int)

    def test_player_with_multiple_games(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("SELECT idgame FROM player WHERE first_name='John'")
        player_id = cursor.fetchone()[0]
        cursor.execute('''
            INSERT INTO game (idgame, idset, date1, hour1, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_id, 2, '2025-10-24', '10:00:00', 30))
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM game WHERE idgame=?", (player_id,))
        game_count = cursor.fetchone()[0]
        assert game_count >= 2


@pytest.mark.integration
class TestCategoryManagement:
    def test_fetch_all_categories(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT domain1 FROM test_set")
        domains = [row[0] for row in cursor.fetchall()]
        assert 'informatics' in domains
        assert 'mathematics' in domains
        assert 'physics' in domains

    def test_get_category_id(self, test_db):
        conn, cursor, db_name = test_db
        cursor.execute("SELECT idset FROM test_set WHERE domain1=?", ('informatics',))
        result = cursor.fetchone()
        assert result is not None
        assert isinstance(result[0], int)

    def test_category_question_association(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT COUNT(*) FROM test t
            JOIN test_set ts ON t.idset = ts.idset
            WHERE ts.domain1 = ?
        ''', ('informatics',))
        count = cursor.fetchone()[0]
        assert count > 0


@pytest.mark.integration
class TestStatistics:
    def test_calculate_average_score(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("SELECT idgame FROM player LIMIT 1")
        player_id = cursor.fetchone()[0]
        scores = [10, 20, 30]
        for score in scores:
            cursor.execute('''
                INSERT INTO game (idgame, idset, date1, hour1, score)
                VALUES (?, ?, ?, ?, ?)
            ''', (player_id, 1, '2025-10-23', '10:00:00', score))
        conn.commit()
        cursor.execute("SELECT AVG(score) FROM game WHERE idgame=?", (player_id,))
        avg_score = cursor.fetchone()[0]
        assert avg_score > 0

    def test_find_highest_score(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute("SELECT MAX(score) FROM game")
        max_score = cursor.fetchone()[0]
        assert max_score >= 15

    def test_count_games_by_category(self, populated_test_db):
        conn, cursor, db_name = populated_test_db
        cursor.execute('''
            SELECT ts.domain1, COUNT(*) as game_count
            FROM game g
            JOIN test_set ts ON g.idset = ts.idset
            GROUP BY ts.domain1
        ''')
        results = cursor.fetchall()
        assert len(results) > 0
        assert all(count > 0 for domain, count in results)


@pytest.mark.integration
class TestInputValidation:
    def test_empty_name_validation(self):
        name = ""
        surname = "Doe"
        selection = "informatics"
        is_valid = bool(name and surname and selection)
        assert is_valid is False

    def test_empty_surname_validation(self):
        name = "John"
        surname = ""
        selection = "informatics"
        is_valid = bool(name and surname and selection)
        assert is_valid is False

    def test_empty_selection_validation(self):
        name = "John"
        surname = "Doe"
        selection = ""
        is_valid = bool(name and surname and selection)
        assert is_valid is False

    def test_valid_input(self):
        name = "John"
        surname = "Doe"
        selection = "informatics"
        is_valid = bool(name and surname and selection)
        assert is_valid is True

    def test_whitespace_only_input(self):
        name = "   "
        surname = "Doe"
        selection = "informatics"
        is_valid = bool(name.strip() and surname and selection)
        assert is_valid is False