# P10_couignoux_julien

![](docs/logo.png)
***

## Sommaire

* [I. Project Introduction](#chapter1)
    * [Application description](#section1_1)
* [II. Project install](#chapter2)
    * [Technologies Used](#section2_1)
    * [Usage](#section2_2)
    * [Note](#section2_3)
* [III. Application usage](#chapter3)

***
## I. Project Introduction <a class="anchor" id="chapter1"></a>

SoftDesk, une société d'édition de logiciels de développement et de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B.

### Application description <a class="anchor" id="section1_1"></a>
Une application de suivi des problèmes pour les trois plateformes (site web, applications Android et iOS).
L'application permettra essentiellement aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.
Les trois applications exploiteront les points de terminaison d'API qui serviront les données.

## II. Project installation <a class="anchor" id="chapter2"></a>

### Technologies Used <a class="anchor" id="section2_1"></a>
* Python3  
* Django4  
* Django Rest Framework

### Usage <a class="anchor" id="section2_2"></a>
* Install python 3: https://www.python.org/downloads/
* Create and activate a virtual env: https://docs.python.org/3/library/venv.html
* Install requirements: pip install -r requirements.txt
* Clone the git project: [git clone](git@github.com:jcouignoux/P10_couignoux_julien.git)
* python django_web_app/manage.py makemigrations
* python django_web_app/manage.py migrate
* python django_web_app/manage.py runserver
* In your web browser enter the address : http://localhost:8000/projects/ or http://127.0.0.1:8000/projects/

### Note <a class="anchor" id="section2_3"></a>
The Secret_Key required for the execution and debugging of project is not removed from the project code. So you can use the project as your college mini-project or by using the project code you can build your own project.
***

## III. Application usage <a class="anchor" id="chapter3"></a>
## Entry point documentation

[Postman documentation](https://documenter.getpostman.com/view/16200204/UzBqnjKn)

* http://127.0.0.1:8000/signup/ : Create a new account
    * POST :
        * username
        * password
        * last_name (not required)
        * for_name (not required)

* http://127.0.0.1:8000/login/ : 
    * POST :
        * username
        * password

* http://127.0.0.1:8000/token/ : get access token and refresh token
    * POST :
        * username
        * password

* http://127.0.0.1:8000/token/refresh/ : refresh access token
    * POST :
        * refresh token

* http://127.0.0.1:8000/projects/ : list or create new project
    * GET : list authorized projects
    * POST :
        * title
        * description
        * type ("B": "BackEnd", "F": "FrontEnd", "I": "iOS", "A": "Android")

* http://127.0.0.1:8000/projects/project_id/ : view details or update own project
    * POST : (only Creator)
        * username
        * password
    * DELETE (only Creator)

* http://127.0.0.1:8000/projects/project_id/users/ : list or create new contributor
    * GET : list authorized projects
    * POST :
        * user
        * role ("A": "Author", "M": "Manager", "C": "Creator")

* http://127.0.0.1:8000/projects/project_id/users/user_id/ : view details or update contributor
    * POST : (only Creator)
        * user
        * role ("A": "Author", "M": "Manager", "C": "Creator")
    * DELETE (only Creator)

* http://127.0.0.1:8000/projects/project_id/issues/ : list or create new contributor
    * GET : list authorized issues
    * POST :
        * title
        * desc
        * tag ("B": "Bug", "I": "Improvement", "T": "Task")
        * priority ("H": "Hight", "M": "Medium"), "L": "Low")
        * status ("T": "ToDo", "I": "InProgress", ("C": "Closed")
        * assignee_user_id

* http://127.0.0.1:8000/projects/project_id/issues/issue_id/ : view details or update own issue
    * POST : (only author_user_id)
        * title
        * desc
        * tag ("B": "Bug", "I": "Improvement", "T": "Task")
        * priority ("H": "Hight", "M": "Medium"), "L": "Low")
        * status ("T": "ToDo", "I": "InProgress", ("C": "Closed")
        * assignee_user_id
    * DELETE (author_user_id)

* http://127.0.0.1:8000/projects/project_id/issues/issue_id/comments/ : list or create new comment
    * GET : list authorized comments
    * POST :
        * description

* http://127.0.0.1:8000/projects/project_id/issues/issue_id/comments/comment_id/ : view details or update own comment
    * POST : (only author_user_id)
        * description
    * DELETE (author_user_id)
