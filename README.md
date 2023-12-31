# Django-project
## About
This project shows election results using django. 
Election results are listed by city and country. Pie chart graphs are available. 

***Sample data is available in this project.***

### Technologies
* Django (4.2)
* PostgreSql
* Matplotlib
* Bootstrapt
* Docker
* HTML/CSS
* AJAX
## Installation
### Running

```
cd my_project
python manage.py runserver
```

### Running using Docker
1. Docker must be installed on the system.
2. Env files should be added.
2. Docker commands
```
docker-compose build
docker-compose up
```
Follow these steps and, postgre and web applications will work
## Admin Panel
Candidates, election results etc. can be added from the admin panel.
```
python manage.py createsuperuser
http://localhost:8000/admin
```
