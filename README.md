# Dating App
REST API - для сервиса знакомств.
### Описание
Приложение для знакомств, где можно просматривать различных пользователей и ставить им симпатию. При взаимной симпатии участники получают об этом уведомление на почту.
### Технологии
Python, Django, DRF, DRF-Simple JWT, Django-filter
### Запуск проекта в dev-режиме
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/AlexMiller93/Dating_app.git
cd ..

```
- Установка и активируйте виртуальное окружение:

```
python3 -m venv venv
venv/Scripts/activate
python -m pip install --upgrade pip
```
- Установка зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Перейдите в каталог с файлом manage.py выполните команды:

Выполнить миграции:

```
python manage.py migrate
```
Создать супер-пользователя:

```
python manage.py createsuperuser
```
Соберить статику:

```
python manage.py collectstatic
```
Тестовые пользователи:

```
python manage.py load_users
```
Запуск проекта:

```
python manage.py runserver
```

### Применение REST API

Доступны всем пользователям.

```
api/clients/create/ - создание пользователя,
```
Доступ авторизованным пользователям.

```
api/clients/token/ - получить токен,
api/clients/token/refresh/ - обновление токена,
api/list/ - просмотр других пользователей,
api/clients/{id}/match/ - оценка пользователя
api/clients/get_geolocation/ - определяет геолокацию по IP,
api/clients/set_geolocation/ - устанавливают заданную геолокацию,
```

Регистрация пользователя:
```
api/clients/create/
{
	"emal": "your_email",
	"password": "your_password",
	"first_name": "first_name",
	"last_name": "last_name",
	"gender": "M" or "W"
}