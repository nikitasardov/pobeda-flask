import pytest

@pytest.mark.api
@pytest.mark.smoke
def test_health_200(client): # Тест для проверки работоспособности эндпоинта /health
    resp = client.get('/health') # Выполняем GET-запрос к эндпоинту /health
    assert resp.status_code == 200 # Проверяем, что статус ответа 200
    assert resp.json() == {'status': 'ok'} # Проверяем, что ответ содержит JSON с полем 'status' равным 'ok'