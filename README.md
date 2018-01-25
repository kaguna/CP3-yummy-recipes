[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6ff3a32c90e04312b28de6b4b7393057)](https://www.codacy.com/app/kaguna/Flask-API?utm_source=github.com&utm_medium=referral&utm_content=kaguna/Flask-API&utm_campaign=badger)
[![Build Status](https://travis-ci.org/kaguna/Flask-API.svg?branch=ft-Test-all-recipe-methods-153892177)](https://travis-ci.org/kaguna/Flask-API)
[![Coverage Status](https://coveralls.io/repos/github/kaguna/Flask-API/badge.svg?branch=ft-Document-recipes-endpoints-154020821)](https://coveralls.io/github/kaguna/Flask-API?branch=ft-Document-recipes-endpoints-154020821)
# Flask-API
## Introduction
The Yummy-Recipes flask Api is a token based application that provides the user with the registration fields for 
the user. To access the resources of the application, the registered user must provide the actual details for 
the authentication. Once the user is authenticated, he/she gets the authority to manipulate the categories and the 
recipes in the application. Below are the steps and descriptions to make sure the application to make sure that the 
application is up and running.

## Features

- Register Users modules
- Login users modules
- User Create, View, Edit and Delete categories modules
- User Create, View, Edit and Delete recipes modules

## Prerequisites

- Python 3.6 and above
- Flask 
- Postman
- Postgres database

## Installation
Open the terminal and navigate to the desired project folder:

``cd <your directory>``

Using SSH method:

``git clone git@github.com:kaguna/Flask-API.git``

Using HTTPS method:

``git clone https://github.com/kaguna/Flask-API.git``

or download the repository from ``https://www.github.com/kaguna`` and 
transfer the folder to the working directory.

- Move to the working directory

``cd <working directory>``

- Install the virtual environment

``pip install virtualenv``

- Create the virtual environment

``python3 -m venv <name of choice>``

- Activate the virtual environment

``source <name of choice>/bin/activate``

- Install all the required packages 

``pip install flask``

- Create the requirements containing packages file by

``pip freeze > requirements.txt``

- Deactivate the virtual environment to install packages

``deactivave``

- Install project requirements

``pip install -r requirements.txt``

- Create a postgres database 

- Change the URL location of the database in the

``instance/config.py``

- Run the application

``(<virtualenv>) ~$ <project directory> python run.py``

## Running tests

- To run tests

``(<virtualenv>) ~$ <project directory> pytest --cov=tests/``

## API Endpoints

### User Authentication


|    URL Endpoints             | HTTP Requests | Description                                      | Public Access  |
|------------------------------|---------------|--------------------------------------------------|----------------|
|    POST auth/register/       | POST          | Create a new user                                |  TRUE          |
|    POST auth/login/          | POST          | Generate token and grant access to the resources |  TRUE          |
|    POST auth/logout/         | POST          | Logout use and revoke access                     |  TRUE          |
|    POST auth/reset-password/ | POST          | Reset user's password                            |  TRUE          |


### Categories


|    URL Endpoints                 | HTTP Requests | Description                                   | Public Access |
|----------------------------------|---------------|-----------------------------------------------|---------------|
|    POST categories/              | POST          | Create a new category                         |  FALSE        |
|    GET categories/               | GET           | Retrieve specific user's paginated categories |  FALSE        |
|    GET category/<category_id>    | GET           | Retrieve specific user category               |  FALSE        |
|    PUT category/<category_id>    | PUT           | Edit a category name                          |  FALSE        |
|    DELETE category/<category_id> | DELETE        | Delete a category                             |  FALSE        |

### Recipes


|    URL Endpoints                                   | HTTP Requests | Description                                   | Public Access |
|----------------------------------------------------|---------------|-----------------------------------------------|---------------|
|    POST category/<category_id>/recipes/            | POST          | Create a new recipe                           |  FALSE        |
|    GET category/<category_id>/recipes/             | GET           | Retrieve specific category's paginated recipes|  FALSE        |
|    GET category/<category_id>/recipe/<recipe_id>   | GET           | Retrieve specific category recipe             |  FALSE        |
|    PUT category/<category_id>/recipe/<recipe_id>   | PUT           | Edit a recipe name                            |  FALSE        |
|    DELETE category/<category_id>/recipe/<recipe_id>| DELETE        | Delete a recipe                               |  FALSE        |


