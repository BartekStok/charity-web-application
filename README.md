# Charity app

Charity application for unused/unwanted things disposal.

Made on completion of a programming course Back-End Python Developer.

## Getting started

Try this app online on Heroku (not yet started)

### Prerequisites

Used technologies:

```
$ Python 3.6
```

### Installing

It is best to use the python `virtualenv` tool to build locally:

```sh
$ git clone https://github.com/BartekStok/charity-web-application
$ cd charity
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python manage.py runserver
```

Then visit `http://localhost:8000` to view the app. Alternatively you
can use gunicorn to run the server locally.


## License

This project is licensed under the MIT License 



- Copyright 2020 © Bartłomiej Stokłosa
