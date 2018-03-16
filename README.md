Adaptive Application
==
This is related to Addaptive application. 
Requires Django 1.11.11 or 2.0.x , Python 3.5 and requests package to be installed.
News is fetched from newsapi.org for Ireland country.

To test
--
Open the project in IDE and run the test. If using pycharm-
* Goto newsrecoapp/application/tests.py
* Right click on `class TestDataRetrieval(TestCase):`
* Select run.

Inorder to run DJango server- 
--
* Goto terminal and in the directory adaptiveapp/newsrecomapp type
`python3 manage.py runserver`

This should run the django server. You can access it on -
`localhost:8000`
