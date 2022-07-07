# Teacher's Directory App

- Create Virtual Env

`python -m pip install --user virtualenv`

`py -m venv <venv>`

- Activate

`.\<venv>\Scripts\activate`

- Install Required Packages

`pip install -r requirements.txt`

- cd to teacher_directory (cd to inside the project)

`cd teacher_directory`

- Make migration files and migrate it, Makesure db.sqlite3 is created in you project directory

`python manage.py makemigrations`

`python manage.py migrate`

- Create Superuser if needed else ignore

`python manage.py createsuperuser`


- Runserver
`python manage.py runserver`

        - url : http://127.0.0.1:8000/

or

`python manage.py runserver <port_no>`

        - url : http://127.0.0.1:<port_no>/