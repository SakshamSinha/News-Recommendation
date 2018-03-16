Adaptive Applicatoin
==
This is related to Addaptive application. 
Requires Django 1.11.11 or 2.0.x , Python 3.5, Textrazor and requests package to be installed.
News is fetched from newsapi.org for Ireland country.
TextRazor is used to do text analysis for keyword extraction.
TextRazor allows only 500 requests per day on free account.

To install TextRazor
--
* Type `pip install textrazor`

To test News Retrieval
--
Open the project in IDE and run the test. If using pycharm-
* Goto newsrecomapp/application/tests.py
* Right click on `class TestDataRetrieval(TestCase):`
* Select run.

To test Text Razor Keyword Extraction
--
Open the project in IDE and run the test. If using pycharm-
* Goto newsrecomapp/application/tests.py
* Right click on `class TestTextExtractor(TestCase):`
* Select run.


Inorder to run DJango server- 
--
* Goto terminal and in the directory adaptiveapp/newsrecomapp and type
`python3 manage.py runserver`

This should run the django server. You can access it on -
`localhost:8000`
