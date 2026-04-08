import os  # Импортируем модуль os, чтобы читать переменные окружения.
# Имя приложения для заголовка API-документации и идентификации сервиса.
APP_NAME = os.environ.get("FASTAPI_APP_NAME", "fastapi-app")
# Адрес хоста, на котором будет слушать сервер (0.0.0.0 = доступ извне контейнера/машины).
HOST = os.environ.get("FASTAPI_HOST", "0.0.0.0")
# Порт запуска; по умолчанию 5000, чтобы совпадать с docker/nginx-конфигурацией проекта.
PORT = int(os.environ.get("FASTAPI_PORT", "5000"))

# BASE_DIR — корневая директория проекта (используется для построения абсолютных путей к файлам/папкам).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_DIR — папка для хранения всех данных приложения (например, базы данных).
DATA_DIR = os.path.join(BASE_DIR, "data")
# DATABASE — путь к файлу sqlite-базы пользователей (data/users.db).
DATABASE = os.path.join(DATA_DIR, "users.db")