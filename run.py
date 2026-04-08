import uvicorn  # Импортируем Uvicorn как ASGI-сервер для запуска FastAPI.
import os  # Импортируем os для чтения переменной включения reload-режима.
from app.config import HOST, PORT  # Импортируем параметры хоста и порта из конфигурации.
if __name__ == "__main__":  # Запускаем сервер только при прямом запуске файла, а не при импорте.
    reload_enabled = os.environ.get("FASTAPI_RELOAD", "0") == "1"  # Включаем hot-reload только при явном FASTAPI_RELOAD=1.
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=reload_enabled)  # Стартуем приложение app из модуля app.main.
