import sqlite3

from app.models import (
    get_connection, init_db, seed_db,
    get_all_users, get_user_by_id, create_user,
)


class TestGetConnection:

    def test_returns_connection(self):
        conn = get_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    def test_row_factory_is_row(self):
        conn = get_connection()
        assert conn.row_factory is sqlite3.Row
        conn.close()


class TestInitDb:

    def test_creates_users_table(self):
        init_db()
        conn = get_connection()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        assert cursor.fetchone() is not None
        conn.close()

    def test_seeds_on_empty_table(self):
        init_db()
        conn = get_connection()
        count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        assert count == 5
        conn.close()

    def test_no_duplicate_seed_on_second_call(self):
        init_db()
        init_db()
        conn = get_connection()
        count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        assert count == 5
        conn.close()


class TestSeedDb:

    def test_inserts_five_records(self):
        conn = get_connection()
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        seed_db(conn)
        count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        assert count == 5
        conn.close()


class TestGetAllUsers:

    def test_returns_list_of_dicts(self):
        init_db()
        users = get_all_users()
        assert isinstance(users, list)
        assert len(users) == 5
        assert all(isinstance(u, dict) for u in users)

    def test_dict_keys(self):
        init_db()
        user = get_all_users()[0]
        assert set(user.keys()) == {'id', 'name', 'email'}

    def test_empty_table_returns_empty_list(self):
        conn = get_connection()
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

        assert get_all_users() == []


class TestGetUserById:

    def test_existing_user(self):
        init_db()
        user = get_user_by_id(1)
        assert user is not None
        assert user['id'] == 1
        assert 'name' in user
        assert 'email' in user

    def test_nonexistent_user_returns_none(self):
        init_db()
        assert get_user_by_id(999) is None


class TestCreateUser:

    def test_creates_and_returns_user(self):
        init_db()
        user = create_user('Тест Тестов', 'test@example.com')
        assert isinstance(user, dict)
        assert user['name'] == 'Тест Тестов'
        assert user['email'] == 'test@example.com'
        assert 'id' in user

    def test_id_auto_increments(self):
        init_db()
        u1 = create_user('Первый', 'first@example.com')
        u2 = create_user('Второй', 'second@example.com')
        assert u2['id'] == u1['id'] + 1
