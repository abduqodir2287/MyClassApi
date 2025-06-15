# MyClassAPI

**MyClassAPI** — это REST API, разработанный с использованием FastAPI, предназначенный для управления школьными классами, учениками, учителями и пользователями с различными ролями. Поддерживается разграничение прав доступа, аутентификация через JWT, загрузка изображений и кэширование с Redis.

---

## 📌 Описание

Проект **MyClassAPI** предоставляет следующие возможности:

- **Аутентификация и роли:**
  - JWT-аутентификация
  - Поддержка ролей: `user`, `student`, `teacher`, `superadmin`
  - Разграничение доступа в зависимости от роли
- **Управление пользователями**
  - Регистрация, вход
  - Обновление данных
  - Просмотр профиля
- **Классы:**
  - CRUD для классов (название, руководитель, лидер, описание, кабинет и пр.)
- **Ученики:**
  - CRUD операции (только superadmin и teacher)
  - Студенты могут просматривать и обновлять свои данные
- **Учителя:**
  - CRUD для учителей
- **Загрузка изображений:**
  - Локальное хранение изображений учеников и учителей
- **Кэширование:**
  - Использование Redis для ускорения работы с популярными запросами

---

## 🧑‍🤝‍🧑 Роли

| Роль        | Доступ                                                        |
|-------------|---------------------------------------------------------------|
| user        | Только GET-запросы                                            |
| student     | GET-запросы и редактирование своего профиля                   |
| teacher     | Полный доступ к ученикам, частичный к классам                 |
| superadmin  | Полный доступ ко всем сущностям и управлению пользователями   |

---

## ⚙️ Технологии

- **FastAPI** — Backend фреймворк
- **PostgreSQL** — База данных
- **SQLAlchemy** — ORM
- **Alembic** — Миграции
- **Pydantic** — Валидация данных
- **JWT** — Аутентификация
- **Redis** — Кэширование
- **Pytest** — Тестирование
- **Docker + Docker Compose** — Контейнеризация
- **Uvicorn** — ASGI сервер

---

## 🚀 Установка

### 1. Клонируйте проект

```bash
git clone https://github.com/abduqodir2287/MyClassApi.git
cd MyClassAPI
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения
```bash
cp .env.example .env
```
Заполните .env своими значениями.

### 5. Примените миграции
```bash
alembic upgrade head
```

## 🐳 Использование с Docker
```bash
docker-compose up --build
```

После этого API будет доступен по адресу:
http://localhost:8000

Документация
http://localhost:8000/docs


## Автоматическое создание суперпользователя

При первом запуске приложения автоматически создаёт следующий данный:

### 1. Суперпользователь

- **Имя пользователя:** admin
- **Фамилия:** adminov
- **Пароль:** password
- **Роль:** superadmin

Эти данные создаются для упрощения начальной настройки приложения. Если вам нужно изменить эти данные, вы можете сделать это непосредственно в базе данных после первого запуска приложения.


## Использование API:

### Основной эндпоинт:
- **GET http://127.0.0.1:8000/Class/class_name**
- **Пример ответа:**
    ```json
    {
      "id": 0,
      "class_name": "string",
      "students_count": 0,
      "school_year": "string",
      "teacher_info": {
        "username": "string",
        "firstname": "string",
        "lastname": "string",
        "birthDate": {
          "date": "01-01-2007"
        },
        "age": 0,
        "gender": "Erkak",
        "subject": "string",
        "idol": "string",
        "bio": "string",
        "social_link": "string",
        "created_at": "2025-06-15T19:18:12.387Z",
        "updated_at": "2025-06-15T19:18:12.387Z"
      },
      "class_leader_info": {
        "username": "string",
        "class_id": 0,
        "firstname": "string",
        "lastname": "string",
        "birthDate": {
          "date": "01-01-2007"
        },
        "age": 0,
        "gender": "Erkak",
        "subject": "string",
        "interests": "string",
        "idol": "string",
        "bio": "string",
        "social_link": "string",
        "created_at": "2025-06-15T19:18:12.388Z",
        "updated_at": "2025-06-15T19:18:12.388Z"
      },
      "all_students": [
        {
          "username": "string",
          "class_id": 0,
          "firstname": "string",
          "lastname": "string",
          "birthDate": {
            "date": "01-01-2007"
          },
          "age": 0,
          "gender": "Erkak",
          "subject": "string",
          "interests": "string",
          "idol": "string",
          "bio": "string",
          "social_link": "string",
          "created_at": "2025-06-15T19:18:12.388Z",
          "updated_at": "2025-06-15T19:18:12.388Z"
        }
      ],
      "description": "string",
      "class_room_number": 0,
      "created_at": "2025-06-15T19:18:12.388Z",
      "updated_at": "2025-06-15T19:18:12.388Z"
    }
  ```

- **В случае несуществующего класса:**
    ```json
    {
      "detail": "Class not found"
    }
    ```

## 📄 Лицензия

### Проект доступен по лицензии MIT. Свободно используйте и дорабатывайте!


