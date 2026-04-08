import sqlite3
import pytest
from app.models import (
    get_connection,
    init_db,
    seed_db,
    get_all_users,
    get_user_by_id,
    create_user
)


class TestGetConnectionDb:
    @pytest.mark.unit
    @pytest.mark.db
    def test_returns_connection(self):
        conn = get_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    @pytest.mark.unit
    @pytest.mark.db
    def test_row_factory_is_row(self):
        conn = get_connection()
        assert conn.row_factory is sqlite3.Row
        conn.close()


class TestInitDb:
    @pytest.mark.unit
    @pytest.mark.db
    def test_creates_users_table(self):
        init_db()
        conn = get_connection()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None
        conn.close()

    @pytest.mark.unit
    @pytest.mark.db
    def test_seeds_on_empty_table(self):
        init_db()
        conn = get_connection()
        count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        assert count == 5
        conn.close()

    @pytest.mark.unit
    @pytest.mark.db
    def test_no_duplicates_seed(self):
        init_db()
        init_db()
        conn = get_connection()
        count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        assert count == 5
        conn.close()


class TestSeedDb:
    @pytest.mark.unit
    @pytest.mark.db
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


class TestGetAllUsersDb:
    @pytest.mark.unit
    @pytest.mark.users
    def test_returns_list_of_dicts(self):
        init_db()
        users = get_all_users()
        assert isinstance(users, list)
        assert len(users) == 5
        assert all(isinstance(u, dict) for u in users)

    @pytest.mark.unit
    @pytest.mark.users
    def test_dict_keys(self):
        init_db()
        user = get_all_users()[0]
        assert set(user.keys()) == {'id', 'name', 'email'}

    @pytest.mark.unit
    @pytest.mark.users
    def test_empty_table(self):
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
        users = get_all_users()
        assert isinstance(users, list)
        assert len(users) == 0


class TestGetUserByIdDb:
    @pytest.mark.unit
    @pytest.mark.users
    def test_existing_user(self):
        init_db()
        user_id = 3
        user = get_user_by_id(user_id)
        assert isinstance(user, dict)
        assert set(user.keys()) == {'id', 'name', 'email'}
        assert user['id'] == user_id

    @pytest.mark.unit
    @pytest.mark.users
    def test_not_existing_user(self):
        init_db()
        user_id = 999
        user = get_user_by_id(user_id)
        assert user is None


class TestCreateUserDb:
    @pytest.mark.unit
    @pytest.mark.users
    def test_returns_dict(self):
        init_db()
        user_name = 'Юрий Гагарин'
        user_email = 'gagarin@example.su'
        new_user = create_user(user_name, user_email)
        assert isinstance(new_user, dict)
        assert set(new_user.keys()) == {'id', 'name', 'email'}
        assert new_user['name'] == user_name
        assert new_user['email'] == user_email

    @pytest.mark.unit
    @pytest.mark.users
    def test_autoincrement(self):
        init_db()
        last_id = max([u['id'] for u in get_all_users()])
        u1_name = 'Юрий Гагарин'
        u1_email = 'gagarin@example.su'
        new_user = create_user(u1_name, u1_email)
        assert new_user['id'] == last_id + 1
        last_id = new_user['id']

        user2_name = 'Алексей Леонов'
        user2_email = 'leonov@example.su'
        new_user = create_user(user2_name, user2_email)
        assert new_user['id'] == last_id + 1
