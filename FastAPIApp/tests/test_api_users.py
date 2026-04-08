import pytest

# Проверяем, что список пользователей доступен и имеет правильный тип
@pytest.mark.api
@pytest.mark.users
def test_get_users_200_and_list(client):
    resp = client.get('/users')  # Выполняем GET-запрос к эндпоинту /users
    assert resp.status_code == 200  # Проверяем, что статус ответа 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 5


# Проверяем получение существующего пользователя
@pytest.mark.api
@pytest.mark.users
def test_get_user_by_id_existing_200(client):
    resp = client.get('/users/1')  # Выполняем GET-запрос к эндпоинту /users/1
    assert resp.status_code == 200  # Проверяем, что статус ответа 200
    data = resp.json()
    assert data['id'] == 1
    assert 'name' in data
    assert 'email' in data


# Проверяем получение несуществующего пользователя
@pytest.mark.api
@pytest.mark.users
def test_get_user_by_id_not_found_404(client):
    # Выполняем GET-запрос к эндпоинту /users/999
    resp = client.get('/users/999')
    assert resp.status_code == 404
    data = resp.json()
    assert 'detail' in data


# Проверяем получение пользователя с невалидным типом ID
@pytest.mark.api
@pytest.mark.users
def test_get_user_by_invalid_id_type_422(client):
    # Выполняем GET-запрос к эндпоинту /users/abc
    resp = client.get('/users/abc')
    assert resp.status_code == 422


# Проверяем создание пользователя с валидными данными
@pytest.mark.api
@pytest.mark.users
def test_post_users_valid_201(client):
    resp = client.post(
        '/users', json={'name': 'Тест', 'email': 'test@example.com'})
    assert resp.status_code == 201
    data = resp.json()
    # Проверяем, что новый id идёт после seed-пользователей.
    assert data['id'] == 6
    assert data['name'] == 'Тест'
    assert data['email'] == 'test@example.com'


# Проверяем создание пользователя с невалидным email через Pydantic
@pytest.mark.api
@pytest.mark.users
def test_post_users_invalid_email_422(client):
    resp = client.post(
        '/users', json={'name': 'Тест', 'email': 'invalid-email'})
    assert resp.status_code == 422

@pytest.mark.api
@pytest.mark.users
def test_post_users_empty_name_422(client):  # Проверяем ограничение min_length
    # передаем пустое имя
    resp = client.post(
        '/users', json={'name': '', 'email': 'test@example.com'})
    assert resp.status_code == 422


# Сквозной сценарий: создание пользователя и проверка, что он появился в списке
@pytest.mark.api
@pytest.mark.users
def test_post_then_users_contains_new(client):
    client.post('/users', json={'name': 'Новый', 'email': 'test@example.com'})
    # Получаем список пользователей после добавления нового
    resp = client.get('/users')
    # Получаем список имён пользователей
    names = [u['name'] for u in resp.json()]
    assert 'Новый' in names
