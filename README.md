# Dines Test

For this test I decided to utilise Django, this was my first time utilising it however I wanted to do the project using it in order to show my aptitude for learning new frameworks. I approached this utilising primarily rest framework's API Views as it provides a comprehensive solution for handling requests while allowing you to overwrite it's functions to implement custom behaviours. The database is the default Django SQL Lite, the reason for this is just simplicity in getting it sent over to you. I have however done research on how to connect a Django app through to other databases and additionally have experience using SQL Alchemy in the past with Flask.

## Modules

From your command line, CD to the directory you have extracted this test to and run the following using pip

```bash
pip install -r requirements.txt
```
For transparency, this project uses Django, django-filter and the django rest framework.

## Running the project

From your command line, CD to the directory you have extracted this test to and run the following command

```bash
python3 manage.py runserver
```

If you would like to run the tests I have included, please feel free to run
```bash
python3 manage.py test
```
For Unit testing, I used Rest Framework's APITestCase modules in order to test that all of my endpoints correctly meet the provided criteria.

## Admin
You can login to the admin console from [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) using the username admin and the password DinesTest1

## API Documentation
You can find basic postman documentation at [this link](https://documenter.getpostman.com/view/23936469/2s84LUQqES) 
