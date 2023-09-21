
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Описание проекта

Сайт с возможностью публикации фотографий котиков.

## Технологии

- Python 3.9
- Django 3.2.3
- Django REST framework 3.12.4
- JavaScript

## Запуск проекта из образов с Docker hub

Для запуска необходимо создать папку проекта и перейти в нее:

```bash
mkdir kittygram
cd kittygram
```

В папку проекта (на действующем сервере или локальной машине) скачиваем файл `docker-compose.production.yml` и запускаем его:

```bash
sudo docker compose -f docker-compose.production.yml up
```

В результате выполнится скачивание образов с Docker Hub, создание и включение контейнеров, создание томов и сети.

## Запуск проекта из исходников GitHub

Клонируем к себе репозиторий: 

```bash 
git clone git@github.com:Sergey-Zaitsev/kittygram_final.git
```

Выполняем запуск:

```bash
sudo docker compose -f docker-compose.yml up
```

## Миграции, сбор статистики

После запуска необходимо выполнить сбор статистики и миграции. Статистика фронтенда собирается во время запуска контейнера, после чего он останавливается. 

```bash
sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py migrate

sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py collectstatic

sudo docker compose -f [имя-файла-docker-compose.yml] exec backend cp -r /app/collected_static/. /static/static/
```

После корректного выполнения указанных команд, роект доступен на: 

```
http://localhost:9000/
```
## Необходимые переменные окружения

```bash
POSTGRES_USER= <Желаемое_имя_пользователя_базы_данных>
POSTGRES_PASSWORD= <Желаемый_пароль_пользователя_базы_данных>
POSTGRES_DB= <Желаемое_имя_базы_данных>
DB_HOST=
DB_PORT= 
SECRET_KEY = 
DEBUG = 
```

## Основные команды для управления.


```bash
sudo docker compose stop
```
Команда остановит все контейнеры, но оставит сети и volume. 
Эта команда пригодится, чтобы перезагрузить или обновить приложения.

```bash
sudo docker compose down
```
Команда остановит все контейнеры, удалит их, сети и анонимные volumes. 

```bash
sudo docker compose logs
```
Команда просмотра логов запущенных контейнеров.

## Автор

Сергей Зайцев https://github.com/Sergey-Zaitsev