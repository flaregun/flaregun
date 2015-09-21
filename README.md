# flaregun
User location sharing prototype
* Create an API that allows users to share their location
* Create a page that displays that location (even if roughly) on a map
* Allow the location markers to be clicked and display extra information

Stolen Heavily from
===================
The Django Rest Framework tutorial: http://www.django-rest-framework.org/tutorial/1-serialization/

Set Up
======
This prototype requires both Django and the Django Rest Framework
and would run best in a virtualenv:

1. mkdir testsite; cd testsite
1. virtualenv env
1. source env/bin/activate
1. pip install django
1. pip install djangorestframework
1. git clone https://github.com/flaregun/flaregun.git

Then set up the database and some test data using the exercise-setup scripts:

1. cd flaregun
1. bash exercise-setup # will migrate the db and set up test data
1. python manage.py runserver
1. open your browser at localhost:8000
1. sign in as admin:345admin
1. explore the test data

To see the locations on a U.S. map:

1. open your browser at localhost:8000/map
