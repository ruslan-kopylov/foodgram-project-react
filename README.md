# Дипломный проект [Foodgram]

Доступ к админке:
login - admin
password - admin

***
Foodgram - cайт для размещения рецептов от пользователей.
***

## Возможности.
* Регистрация на сайте
* Создание пользовательских рецептов.
* Подписка на других пользователей.
* Добавление рецептов в избранное.
* Добавление рецептов в корзину покупок с возможностью скачать список ингредиентов с граммовкой.
***

## Установка.
***
Клонировать репозиторий.

```
git clone git@github.com:ruslan-kopylov/foodgram-project-react.git

```
В папку foodgram-project-react/infra/ положить файл .env:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432 
```

Запустить контейнеры:

```
sudo docker-compose up -d 
```

Зайти в контейнер, выполнить миграции, загрузить теги и ингредиенты в базу данных:

```
sudo docker exec -it infra-backend-1 bash

python manage.py migrate

python manage.py loaddata
```
Фронт доступен по адресу :

```
https://localhost/
```
Документация API доступна по адресу :

```
http://localhost/api/docs/
```

[Foodgram]:http://51.250.26.145/signin
