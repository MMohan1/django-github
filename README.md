# django-tutorial

Django tutorial application built using Requests, Bower, Twitter Bootstrap and Github API

# Installation

To install the required libraries for this file, simply run the following:

    pip install -r requirements.txt

This project also requires using Bower, which requires NPM. In order to get NPM, simple install <a href="https://nodejs.org/download/">Node.js</a>. Once you have node, you can install <a href="http://bower.io/">Bower</a>:

    npm install -g bower

**Note**: On a Mac, you'll need to use:

    sudo npm install -g bower

With Bower, you can install the front-end dependencies by running:

    bower install

This will generate the **static** folder along with **bootstrap** and **jquery** inside it.


# Running the project

To run this project:


    # Setup the database
    python manage.py migrate
    python manage.py makemigrations

    # Run the server
    python manage.py runserver

You can now visit the following URLS:

	* http://127.0.0.1:8000/github/search/

# Tests

Run the test suite:

    python manage.py test


# Developer Setup

default app setup is developer setup.the set up settings are in the githuppapi/settings.py file.
        DEVELOPER_SETUP
        MAX_GITHUB_SEARCH

    The DEVELOPER_SETUP is boolena that means is set is developer or Prod.
    MAX_GITHUB_SEARCH - maximaum how many search results will be store in developer data base. The max size is 100.    
    

#Producation SetUp

Prdocation setup require the <a href="https://www.rabbitmq.com/download.html"> Rabbitmq </a> and python <a href="http://www.celeryproject.org/"> Celery</a>.
The <a href "http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html"> celery Configuration </a> is require to run the app. Once the rabbitmq and celey setup done. change the githuppapi/settings.py DEVELOPER_SETUP to False to search and store the results in background.



# Results

To see the stored results Follow the stapes-
   # create superuser
   python manage.py createsuperuser
   # You can now visit the following URLS:
   * http://127.0.0.1:8000/admin/
   