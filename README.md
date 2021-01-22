# Django Blog

This is a simple django blog project.


## How to setup

____
Create virtual environment (Optional)
```shell
python -m venv env
env\Scripts\activate
```

Install requirements

```shell
python -m pip install -r requirements.txt
```

Make migrations
```shell
python manage.py makemigrations interaction account category blog
```

Migrate the database
```shell
python manage.py migrate
```
___

TODO: Add sample data to import on setup