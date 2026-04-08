import uvicorn  # Импортируем Uvicorn как ASGI-сервер для запуска FastAPI.
from app.config import HOST, PORT  # Импортируем параметры хоста и порта из конфигурации.
if __name__ == "__main__":  # Запускаем сервер только при прямом запуске файла, а не при импорте.
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)  # Стартуем приложение app из модуля app.main с автоперезапуском при изменениях.
