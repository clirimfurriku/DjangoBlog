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

## Included data

---

### What is included 
- Sample posts
- A banned post
- Sample categories
- Sample comments on posts
- Admin account 
``username: admin
  password: 123456``
- User account 
``username: reader
  password: ReaderDemoPassword132``


### How to import the included data:
Run this command to add the data to the database
```shell
python manage.py loaddata to_import.json
```

Start the server
```shell
python manage.py runserver
```


## How to run tests

---

To run tests run the command below
```shell
python maanage.py test
```