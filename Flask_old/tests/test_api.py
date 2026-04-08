import json


class TestGetUsers:

    def test_status_200(self, client):
        resp = client.get('/users')
        assert resp.status_code == 200

    def test_returns_json_list(self, client):
        resp = client.get('/users')
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) == 5

    def test_user_fields(self, client):
        resp = client.get('/users')
        user = resp.get_json()[0]
        assert set(user.keys()) == {'id', 'name', 'email'}


class TestGetUserById:

    def test_existing_user(self, client):
        resp = client.get('/users/1')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['id'] == 1
        assert 'name' in data
        assert 'email' in data

    def test_nonexistent_user_404(self, client):
        resp = client.get('/users/999')
        assert resp.status_code == 404
        data = resp.get_json()
        assert 'error' in data


class TestPostUsers:

    def test_valid_data_201(self, client):
        resp = client.post('/users', json={'name': 'Тест', 'email': 'test@example.com'})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['name'] == 'Тест'
        assert data['email'] == 'test@example.com'
        assert 'id' in data

    def test_empty_name_400(self, client):
        resp = client.post('/users', json={'name': '', 'email': 'test@example.com'})
        assert resp.status_code == 400
        assert 'error' in resp.get_json()

    def test_invalid_email_400(self, client):
        resp = client.post('/users', json={'name': 'Тест', 'email': 'not-an-email'})
        assert resp.status_code == 400
        assert 'error' in resp.get_json()

    def test_no_body_400(self, client):
        resp = client.post('/users', content_type='application/json')
        assert resp.status_code == 400
        assert 'error' in resp.get_json()

    def test_missing_fields_400(self, client):
        resp = client.post('/users', json={})
        assert resp.status_code == 400


class TestPostThenGet:

    def test_created_user_appears_in_list(self, client):
        client.post('/users', json={'name': 'Новый', 'email': 'new@example.com'})
        resp = client.get('/users')
        names = [u['name'] for u in resp.get_json()]
        assert 'Новый' in names

    def test_created_user_accessible_by_id(self, client):
        post_resp = client.post('/users', json={'name': 'Прямой', 'email': 'direct@example.com'})
        user_id = post_resp.get_json()['id']
        get_resp = client.get(f'/users/{user_id}')
        assert get_resp.status_code == 200
        assert get_resp.get_json()['name'] == 'Прямой'
