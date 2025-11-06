# Service for football stats
## Team
* Kasimov Roman, B22-515 st

## Description
Service for making predictions for internetional football events and competitions with other players

## Technology stack
### Backend (Server side)
* Programming language: **Python**
* Web-Framework: **Django**
* ORM (Object-Relational Mapping): **Django ORM**
* API Framework: **Django Rest Framework**

### Frontend (Client side)
* Programming language: **JavaScript**
* Framework: **HTML/CSS/JS**

### Database
* **Postgres16**

### Other
* Dependencies control system for Python: **poetry**
* Dependencies control system for JS: **npm**
* IDE: **VSCode**
* Tests: **unittest**
* Linter: **ruff**

### How to
#### Clone project from git
`git clone https://gitlab.digital.mephi.ru/kasimovrom/football-results`
`cd football-results`

#### Install dependencies with poetry
`poetry install`

#### Create a python virtual environment
`python3 -m venv env`
s`ource env/bin/activate`  # On Windows use `env\Scripts\activate`
\# Or use `poetry shell`

#### Run migrations
`python manage.py migrate`

#### Create superuser
`python manage.py createsuperuser`

#### Run dev server
`python manage.py runserver`