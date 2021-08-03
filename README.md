MyCar Assessment
================

[mycar.kz](https://mycar.kz) assessment assignment.

Points of Interest
------------------

**./cars/management/commands/_scraper.py** - scraper module, scrapes car data from [mycar.kz](https://mycar.kz).

**cars.views.search** - actual search method, connected to cars?search=<search term> path.

Insights
--------

The actual search uses **django.contrib.postgres.search** module. The module utilizes
[Full Text Search](https://www.postgresql.org/docs/current/textsearch.html) capabilities of PostgreSQL.

Views, serializers, and routers are generated with [drf_generators](https://pypi.org/project/drf-generators/).

Run
---

**Requires PostgreSQL 11 or higher.**

Environment variables:

```shell
$ export DB_NAME=<db_name>
$ export DB_USER=<db_user>
$ export DB_PASSWORD=<db_password>
```

Run the server:

```shell
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py importcars      # scrapes data from mycar.kz and imports it into PostgreSQL
$ python manage.py runserver
```

Example query in browser.

> localhost:8000/cars?search=Toyota
