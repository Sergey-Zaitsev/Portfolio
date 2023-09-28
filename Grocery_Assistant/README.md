
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Описание проекта

Проект Foodgram "Продуктовый помощник" - платформа для публикации рецептов.

## Технологии

- Python 3.11
- Django 4.2.4
- Django REST framework 3.14.0
- JavaScript

#### Проект состоит из следующих страниц: 

- главная
- страница рецепта
- страница пользователя
- страница подписок
- избранное
- список покупок
- создание и редактирование рецепта

#### Структура репозитория
 * В папке frontend находятся файлы, необходимые для сборки фронтенда приложения.
 * В папке infra — заготовка инфраструктуры проекта: конфигурационный файл nginx и docker-compose.yml.
 * В папке backend бэкенд продуктового помощника.
 * В папке data подготовлен список ингредиентов с единицами измерения. Список сохранён в форматах JSON и CSV.
 * В папке docs — файлы спецификации API.

#### Базовые модели проекта

**Рецепт**

 * Автор публикации (пользователь).
 * Название.
 * Картинка.
 * Текстовое описание.
 * Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
 * Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
 * Время приготовления в минутах.

**Тег**

 * Название.
 * Цветовой HEX-код.
 * Slug.

**Ингредиент**

 * Название.
 * Количество.
 * Единицы измерения.

#### Сервис "Список покупок"
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

## Установка

Для запуска необходимо установить Docker и Docker Compose.  
Подробнее об установке на различных платформах можно узнать на [официальном сайте](https://docs.docker.com/engine/install/).

1. Клонируйте проект:
```
git clone git@github.com:Sergey-Zaitsev/foodgram-project-react.git
```

2. Скачайте и установите curl — консольную утилиту, которая умеет скачивать файлы по команде пользователя:
```bash
sudo apt update
sudo apt install curl
```

3. Скачать и выполнить скрипт:
```bash
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

4. Проверить что  Docker работает можно командой:
```bash
sudo systemctl status docker
```
5. Подготовить переменные окружения:

В директории infra, есть шаблон .env.example по заполнению файла.
```
scp .env <username>@<host>:/home/<username>/
```

6. Собрать контейнеры и выполните миграции:
```
sudo docker compose up -d --build
sudo docker compose exec backend python manage.py migrate
```
7. Создать суперюзера и собрать статику:
```
sudo docker compose exec backend python manage.py createsuperuser
sudo docker compose exec backend python manage.py collectstatic --no-input
```
8. Заполняем базу ингредиентами и тегами:
```bash
sudo docker compose exec backend python manage.py loaddata --path 'recipes/data/ingredients.json'
```

## Автор

Сергей Зайцев https://github.com/Sergey-Zaitsev

Развернутый проект:
```
https://foodgram196.myddns.me
```
Для входа в Admin панель необходимо воспользоваться следующей учетной записью:
Админпанель:
```
https://foodgram196.myddns.me/admin/
```
