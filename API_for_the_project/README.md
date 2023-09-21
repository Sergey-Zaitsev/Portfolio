
# API для проекта Yatube спринт 9 (Яндекс.Практикум)

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

### Описание проекта:

Проект представляет собой API для проекта yatube.

Функционал:
Авторизация по JWT токену

Обработка GET, POST, PATCH, PUT и DELETE запросов к базе данных проекта Yatube

### Технологии
- Python 3.9
- Django 3.2
- DRF 3.12
- PyJWT 2.1.

### Запуск проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VadimVolkovsky/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python3 manage.py migrate
```

Запустить проект:

```bash
python3 manage.py runserver
```

### Примеры запросов к API:

Получение токена

Отправить POST-запрос на адрес `api/v1/jwt/create/` и передать 2 поля в `data`:

1. `username` - имя пользователя.
2. `password` - пароль пользователя.

Создание поста

Отправить POST-запрос на адрес `api/v1/posts/` и передать обязательное поле `text`, в заголовке указать `Authorization`:`Bearer <токен>`.

1. Пример запроса:

   ```json
   {
     "text": "Мой пост."
   }
   ```

2. Пример ответа:

   ```json
   {
     "id": 2,
     "author": "Sergey",
     "text": "Мой пост.",
     "pub_date": "2023-04-19T09:00:22.021094Z",
     "image": null,
     "group": null
   }
   ```

Комментирование поста пользователя

Отправить POST-запрос на адрес `api/v1/posts/{post_id}/comments/` и передать обязательные поля `post` и `text`, в заголовке указать `Authorization`:`Bearer <токен>`.

1. Пример запроса:

   ```json
   {
     "post": 1,
     "text": "Тест"
   }
   ```

2. Пример ответа:

   ```json
   {
     "id": 1,
     "author": "Sergey",
     "text": "Тест",
     "created": "2023-04-19T09:00:22.021094Z",
     "post": 1
   }
   ```

## Документаия проекта

```bash
http://127.0.0.1:8000/redoc/
```
