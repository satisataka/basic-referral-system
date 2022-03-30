# basic-referral-system
This app is a simple blank for a referral system.
Custom user model with authentication Phone Number (SMS)

To set up the application to send real SMS:
* Setting [django-sms]:(https://github.com/roaldnefs/django-sms)
* Correct `settings.py` SENDSMS_DUBAG = False

## Install

	git clone git@github.com:satisataka/basic-referral-system.git
	cd basic-referral-system
	pip install -r requirements.txt

## Database
	add database settings /invite_django/settings.py

## Run the app

	python manage.py migrate
	python manage.py runserver

	http://localhost:8000/ - Django Template
	http://localhost:8000/api/login/ - Login (Django REST API)
	http://localhost:8000/api/account/ - Account (Django REST API)

# REST API

## Send SMS code

### Request

`POST /api/login/`

    curl -d 'phone_number=+79998889898' http://localhost:8000/api/login/

### Response

	{
		"phone_number":"+79998889898",
		"debug_otp":"5719"
	}

## Get Api Token

### Request

`POST /api/login/`

    curl -d 'otp=5719' http://localhost:8000/api/login/

### Response

	{
		"url_account":"/api/account/",
		"token":"a82d431d9bb2e0890cd8ede9663649fd570e6700"
	}

## Get Account

### Request

`GET /api/account/`

	curl -H 'Authorization: Token a82d431d9bb2e0890cd8ede9663649fd570e6700' http://localhost:8000/api/account/

### Response

	{
		"url_account":"/api/account/",
		"phone_number":"+79879879898",
		"username":"+79879879898",
		"email":"",
		"first_name":"",
		"last_name":"",
		"last_login":"2022-03-30T04:59:02.718663+03:00",
		"date_joined":"2022-03-30T04:59:02.613466+03:00",
		"invite":null,
		"user_invite":{
			"pk":2,
			"key":"CJDbJo",
			"account_set":[]
		}
	}

## Change "username", "email", "first_name", "last_name"

### Request

`PUT /api/account/`

	curl.exe -H 'Authorization: Token a82d431d9bb2e0890cd8ede9663649fd570e6700' -d 'username=Doctor' -X PUT http://localhost:8000/api/account/

### Response

	{
		"phone_number":"+79879879898",
		"username":"Doctor",
		"email":"",
		"first_name":"",
		"last_name":"",
		"last_login":"2022-03-30T04:59:02.718663+03:00",
		"date_joined":"2022-03-30T04:59:02.613466+03:00",
		"invite":null,
		"user_invite":{
			"pk":2,
			"key":"CJDbJo",
			"account_set":[]
		}
	}

## Add "invite" (Added once, cannot be changed later)

### Request

`PUT /api/account/`

	curl.exe -H 'Authorization: Token a82d431d9bb2e0890cd8ede9663649fd570e6700' -d 'invite=qeWd2q' -X PUT http://localhost:8000/api/account/

### Response

	{
		"phone_number":"+79879879898",
		"username":"Doctor",
		"email":"",
		"first_name":"",
		"last_name":"",
		"last_login":"2022-03-30T04:59:02.718663+03:00",
		"date_joined":"2022-03-30T04:59:02.613466+03:00",
		"invite":"qeWd2q",
		"user_invite":{
			"pk":2,
			"key":"CJDbJo",
			"account_set":[]
		}
	}
