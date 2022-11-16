# STOCKWATCH

## Context: 
This repository contain the application I created in order to pass the technical test asked by CodaBene in the case of an intership application.

## Application description: 
This app allows to check the expiring dates of different products. 
It's possible to add a new product or to update its date. You can also search a product in the list thanks to its GTIN to see directly its expiring date.

## REQUIREMENT: 
### Versions:
Django version 4.1.3 / Python 3.10.7 
### Modules:
DateTime 
### DataBase
PostgreSQL is used. It's possible to change the type of DB in *settings.py*. Go to *DATABASES* and change the *dafault* parameters. 
For more information you can check the page: https://docs.djangoproject.com/en/4.1/ref/settings/#databases


## How to use:
### Run the server
Go to your terminal and type: *python ./manage.py runserver* Then you should be able to ctrl+click on the http adress displayed (or copy/past it)
### Migration error
If there is an error on Migration you need to delete files in migration folder and run the next command line: *py.exe ./manage.py makemigrations*

### Debug:
To be able to debug the application, go into the settings.py and change *DEBUG = False* into *DEBUG = True* and *ALLOWED_HOSTS = ['\*']* into *ALLOWED_HOSTS = []*

