# realtime_rest test application

This is a simple application providing a model (`MyModel`) and a rest_framework ViewSet (`MyModelViewSet`). It uses the django-realtime-rest package to allow for [long-polling](https://en.wikipedia.org/wiki/Push_technology#Long_polling).

Clone the repo this way:
```
git clone https://github.com/jdmichaud/rtr
```
Install the environment (you might want to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) before):
```
cd rtr/django-realtime-rest-test/
pip install -r requirements.txt
```

This will install `django`, the `rest_framework` package, `realtime_rest` package and a couple of other dependencies.

Then, migrate the application:
```
python manage.py migrate
```

Then launch the dev server:
```
python manage.py runserver
```

Finally you can test the long-polling feature. First, perform a GET request on the `-rt` url:
```
curl -siL -w'\n' -X GET localhost:8000/api/my-models-rt/ -H 'Content-Type: application/json'
```

The call will block (long-polling).
Then POST something in the database:
```
curl -siL -w'\n' -X POST -d '{ "myField": "test" }' localhost:8000/api/my-models/ -H "Content-Type: application/json"
```

The first curl request will return, displaying the content of the database:
```
HTTP/1.0 200 OK
Date: Fri, 27 Jan 2017 19:46:37 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Allow: GET, POST, OPTIONS

[{"myField":"test"}]
```
