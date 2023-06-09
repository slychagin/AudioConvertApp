# AudioConvertApp
![made by](https://img.shields.io/badge/made_by-slychagin-orange)
![python](https://img.shields.io/badge/python-v3.10.5-blue)
![fastapi](https://img.shields.io/badge/fastapi-v0.95.1-green)
![fastapi-users](https://img.shields.io/badge/fastapi_users-v11.0.0-red)
![postgres](https://img.shields.io/badge/postgres-15-blue)
![pytest](https://img.shields.io/badge/pytest-ok-brightgreen)

API that convert .wav files to .mp3
#
#### Функционал вэб сервиса:
Веб сервис на Python3 (фреймворк FastAPI) со следующими REST методами:
1. Cоздание пользователя (POST):
- для регистрации нового пользователя необходимо указать email, password и username;
- cоздаёт в базе данных пользователя c заданными данными, а также генерирует уникальные идентификатор пользователя и UUID токен доступа для данного пользователя;
- возвращает сгенерированные идентификатор пользователя и UUID токен.
2. Добавление аудиозаписи (POST):
- принимает на вход запросы, содержащие уникальный идентификатор пользователя, UUID токен доступа и аудиозапись в формате wav;
- преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет ее в базу данных;
- возвращает URL для скачивания аудиозаписи вида http://host:port/record?id=id_записи&user=id_пользователя.
3. Доступ к аудиозаписи (GET):
- предоставляет возможность скачать аудиозапись по вышеуказанной ссылке.
4. Кроме стандартной документации Swagger, так же реализован фронтенд.

#
#### Что использовано для создания API:
- вэб сервис реализован на Python3 с помощью FastAPI;
- в качестве СУБД использована PostgreSQL;
- вэб сервис разворачивается в Docker с помощью docker compose;
- протестировано с помощью pytest.

#
#### Примеры запросов POST и GET к API сервиса (фронтенд):
**_Регистрация нового пользователя (POST):_**

![front_create_user](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/front_register.gif)

**_Конвертирование аудиозаписи (POST):_**

![front_post_audio](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/front_conver.gif)

**_Загрузка аудиозаписи по ссылке, полученной при добавлении записи (GET):_**

![front_get_audio](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/front_download.gif)


#
#### Примеры запросов POST и GET к API сервиса (документация Swagger):
**_Регистрация нового пользователя (POST):_**

![create_user](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/create_user.gif)

**_Конвертирование аудиозаписи (POST):_**

![post_audio](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/post_audio.gif)

**_Загрузка аудиозаписи по ссылке, полученной при добавлении записи (GET):_**

![get_audio](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/get_audio.gif)

#
#### Инструкция по настройке и запуску приложения:
- для выполнения данных инструкций у вас должен быть установлен Docker;
- все данные для подключения есть в файле .env-prod (так как приложение тестовое, то данный файл не добавлял в .gitignore);
- в коммандной строке откройте папку, в которую хотите склонировать проект и запустите команду

`git clone https://github.com/slychagin/AudioConvertApp.git`;
- затем перейдите в корневую папку проекта `cd AudioConvertApp`;
- создайте образ Docker `docker compose build`;
- запустите контейнеры `docker compose up` (после выполнения данной команды у вас должны запуститься следующие сервисы: приложение, база данных postgres и pgadmin);
- чтобы зайти в приложение через фронтенд посетите адрес `http://localhost:8888`, документация Swagger - зайдите по адресу `http://localhost:8888/docs`;
- примеры запросов смотрите выше;
- для работы с базой данных в удобном интерфейcе Pgadmin4 необходимо зайти по адресу `http://localhost:5050`, аутентифицироваться введя почту `quiz@quiz.com` и пароль `quiz_777`:

![pgadmin_auth](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/pgadmin_auth.jpg)
- далее создайте новый сервер:

![pgadmin_create_server](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/pgadmin_create_server.jpg)
- в открывшемся окне во вкладке General введите любое имя для сервера:

![pgadmin_enter_name](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/pgadmin_enter_name.jpg)
- в том же окне во вклдаке Connection заполните Host name/address=pg_container, Port=5432, Maintenance database=postgres, Username=postgres, Password=postgres и нажмите Save, чтобы подключиться к серверу. Как вариант, в Host name/address можно ввести не имя контейнера Postgres, а IP адрес. Для чего в командной строке выполните команды `docker ps` -> скопируйте ID или имя контейнера Postgres -> `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id`:

![pgadmin_connection](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/pgadmin_connection.jpg)
- чтобы просмотреть, добавленные в базу данных записи выполните запрос `SELECT * FROM audios;`

![pgadmin_get_data](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/pgadmin_get_data.jpg)
