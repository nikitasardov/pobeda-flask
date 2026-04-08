# Импортируем FastAPI-компоненты: приложение, HTTPException и объект запроса.
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
# Импортируем исключение ошибок валидации входных данных.
from fastapi.exceptions import RequestValidationError
# Импортируем JSONResponse для явного формата ответов обработчика ошибок.
from fastapi.responses import JSONResponse
# Импортируем базовую модель и типы валидации Pydantic.
from pydantic import BaseModel, EmailStr, Field
from app.config import APP_NAME  # Импортируем имя приложения из конфигурации.
from app.models import (
    init_db,
    get_all_users,
    get_user_by_id as get_user_by_id_db,
    create_user as create_user_db  # Импортируем функции работы с SQLite.
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield
    print("Завершение работы приложения")


# Создаём экземпляр FastAPI и задаём заголовок для документации OpenAPI.
app = FastAPI(title=APP_NAME, lifespan=lifespan)


class UserCreate(BaseModel):  # Описываем тело запроса для создания пользователя
    # Имя пользователя обязательно, строка от 1 до 100 символов
    name: str = Field(description="Имя пользователя",
                      min_length=1, max_length=100)
    email: EmailStr  # Поле email: валидный email, проверяется автоматически.


class UserOut(BaseModel):  # Описываем тело ответа при запросе пользователя
    id: int  # ID пользователя
    name: str  # Имя пользователя
    email: EmailStr  # Email пользователя




# Регистрируем GET-эндпоинт /health для проверки "живости" сервиса.
@app.get("/health", tags=["system"])
def healthcheck():  # Объявляем обработчик запроса для эндпоинта /health.
    # Возвращаем простой JSON-ответ, что сервис работает.
    return {"status": "ok"}


# Эндпоинт списка пользователей со схемой ответа
@app.get("/users", response_model=list[UserOut], tags=["users"])
def get_users():  # Функция-обработчик GET /users
    return get_all_users()  # Возвращаем список пользователей


# Эндпоинт получения пользователя по ID со схемой ответа
@app.get("/users/{user_id}", response_model=UserOut, tags=["users"])
def get_user_by_id(user_id: int):  # Функция-обработчик GET /users/{user_id}
    user = get_user_by_id_db(user_id)
    if user is None:  # Если пользователь не найден
        # Если пользователь не найден, возвращаем 404 ошибку
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user  # Возвращаем пользователя



# Эндпоинт создания пользователя со схемой ответа и статусом 201
@app.post("/users", response_model=UserOut, status_code=201, tags=["users"])
def create_user(payload: UserCreate):  # Функция-обработчик POST /users
    # Создаём нового пользователя
    return create_user_db(payload.name, payload.email)
