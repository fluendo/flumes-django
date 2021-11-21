# flumes-django
`Django` application to manage the `flumes` database

## Features
* Seamless integration between `Django` and `flumes`
* Possiblity to upload files directly through the admin interface

## Setup
In order to integrate `flumes-django` into your `Django` application, you need to:

Add `flumes-django` as an installed application in your `settings.py`
```python
INSTALLED_APPS = (
    ...,
    "flumes_django",
)
```

Add the `flumes` database to your `settings.py`, you can do it manually or use the `flume_django.config.FlumesDjangoConfig` helper

```python
from flumes_django.config import FlumesDjangoConfig
config = FlumesDjangoConfig()
DATABASES = {
    "flumes": {
        "ENGINE": config.get_django_database_engine(),
        "NAME": config.get_database_database(),
    },
}
```

Add the `flumes-django` router in your `settings.py`
```python
DATABASE_ROUTERS = ["flume_django.router.Router"]
```

In case the discovery of the files happens in another machine, you can override the path where the files are stored by setting
```python
FLUMES_DJANGO_ROOT = "/your/own/local/path"
```

## Demo
The project has a `demo` folder, in order to run locally, make sure you have a `flumes` configuration in `$HOME/.flumes` or `/etc/flumes` and simply run

```shell
poetry run python manage_demo.py runserver
```
After entering into the admin site, you will see something like this:
![Admin Video](demo/admin-video.png)

## Development
The project is based in `poetry` dependency management and packaging system. The basic steps are

Install poetry
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Install the dependencies
```
poetry install
```

Install your development pre-commit hooks
```
poetry run pre-commit install
```

## References
* [Flumes](https://github.com/turran/flumes)
* [Poetry Template](https://github.com/yunojuno/poetry-template)
