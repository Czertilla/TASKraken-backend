# Lizzard Dangeon Master
## Описание
### Суть
Вся суть в том, что огромная куча поверженных ящеров сидит в подвале под Саратовом.
Если они там просто будут сидет, тол взбунтуются и начнется новы виток насилия. 
Но если занять их делом, эксплуатируя рабочую силу, то всем нам будет жить хорошо.

### Идея
Очень много фотографий с большого колличества камер сможет обрабатывая тоьлко очень большая толпа ящеров. 
Чтобы пропускная способность данных оставалась на высоте вне зависимости от колличества набежавших туристов.
Для этого используется ассинхронное программирование и тесно с ним связанный фреймворк fastAPI

### Замысел
Изначанльный замысел был в разделении на модули:
  Запросы обрабатывают отдельные роутеры, которые в свое очередь вызывают методы классов репозиториев.
  по сути в архитектуре этого проекта два слоя. в дальнейшем планируется добавить третий слой сервисов, хоть для 
  подобного пэт проекта достаточно и двух слоев

## Ход разработки
за ходом разработки можно следить на открытой trello [доске](https://trello.com/b/BGPNMSSk/main) по данному проекту 
Также вы можете посетить другие ветви, чтобы следить за ходом разработки

# инструкция по установке
в понравившейся вам папочке прописываем:
```bash
$ git clone https://github.com/Czertilla/RTUITLrecruitTask.git
```
## используя Docker
Для данного метода необходимо установить и запустить docker на вашей машине

Cоздаем файл с названием ".env-non-dev" с содержимым по следующему шаблону
```bash
DB_HOST=db
DB_PORT=5454
DB_NAME=
DB_USER=
DB_PASS=
DB_DBMS=postgres
USERS_SECTRET=
PASSW_SECTRET=
PYTHONPATH=src;test

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```
теперь строим docker compose из соответсвующего файла
```bash
$ docker compose build
```
Проект  готов к запуску, чтобы это сделать, просто пропишите
```bash
$ docker compose up
```
данные из базы данных сохраняются в тома, поэтому можно смело убрать все контейнеры
по команде
```bash
$ docker compose down
```
## используя вируальное окружение
Для данного метода необходимо установить и запустить PostgreSQL сервер на вашей машине

Необходимо инициализировать виртуальное окружение
```bash
$ py -m venv .venv
```
запустите виртуальное окружение (непосредствено файл .venv\Scripts\Activate.ps1) или
```bash
$ .venv\Scripts\Activate.ps1
```
теперь установите все необходимые библиотеки
```bash
$ pip install -r requirements.txt
```
теперь необходимо создать файл .env и записать туда данные по следующему шаблону
```
DB_HOST = localhost
DB_PORT = 
DB_NAME = 
DB_USER =
DB_PASS = 
DB_DBMS = postgres
USERS_SECTRET = 
PASSW_SECTRET =
```
теперь нужно запустить миграцию базы данных
```bash
$ alembic upgrade head
```

теперь остается только запустить uvicorn сервер и радоваться жизни
```bash
$ uvicorn main:app --reload
```
вы можете комбинировать методы docker и venv
