# README #


### How do I get set up? ###

* Install python 2.7
* Create new project folder and clone the project
* create new virtualenv
* Activate virtualenv and install all requiements by ` pip install -r requirements.txt `
* ` python manage.py makemigrations `
  ` python manage.py migrate `
* `python manage.py runserver`
  ANd you can brose page at localhost:8000
* Celery Task:
  On project root folder run `celery -A preeti worker -l info`

- I have uploaded db sqlite file together so you don't have to do migration actually. 

