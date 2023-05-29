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
- преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет ее в базе данных;
- возвращает URL для скачивания аудиозаписи вида http://host:port/record?id=id_записи&user=id_пользователя.
3. Доступ к аудиозаписи (GET):
- предоставляет возможность скачать аудиозапись по вышеуказанной ссылке.

#
#### Что использовано для создания API:
- вэб сервис реализован на Python3 с помощью FastAPI;
- в качестве СУБД использована PostgreSQL;
- вэб сервис разворачивается в Docker с помощью docker compose;
- протестировано с помощью pytest.

#
#### Примеры запросов POST и GET к API сервиса в документации Swagger:
Регистрация нового пользователя (POST):

![create_user](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/create_user.gif)

Конвертирование аудиозаписи (POST):

![post_audio](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/post_audio.gif)

Загрузка аудиозаписи по ссылке, полученной при добавлении записи (GET):

![get_audio](https://github.com/slychagin/AudioConvertApp/blob/master/demo_gifs/get_audio.gif)

