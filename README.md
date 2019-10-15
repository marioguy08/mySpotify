<p align="center">
  <a href="" rel="noopener">
 <img width=400px height=300px src="https://i.imgur.com/oCHZjSw.png" alt="Project logo"></a>
</p>

<h3 align="center">Spotify Playlist Analytics</h3>


---

<p align="center"> Software Engineering Principles I - Final Project - Team 7
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Tests](#tests)
- [Built Using](#built_using)
- [Authors](#authors)
- [Documentation](#documentation)

## 🧐 About <a name = "about"></a>
Our application generates and visualizes data queried from a user’s Spotify playlist. It describes how happy, sad, energetic, slow, acoustic, electronics, etc. a playlist is, according to Spotify's API.

The application is something of a social network built around Spotify. We generate graphs from the songs in your playlist, and allow you to share them with friends. It's an easy visualizer for the mood, genre, and style of your playlists. 

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

Set up your Python 3 [virtual environment](https://docs.python.org/3/tutorial/venv.html).

### Installing

Install the python dependencies

```
pip install -r requirements.txt
```

(Optional): Check `flask`, `flask-sqlalchemy`, and `flask-End with an example of getting some data out of the system or using it for a little demo.

## 🔧 Tests <a name = "tests"></a>
Eventually, I'd like to have a `./tests` folder, and write Unit Tests for the backend.

#### Test 1

Explain what this test tests and why.

```
Give an example
```

## 🎈 Usage <a name="usage"></a>
Run the flask server

```
python run.py
```

## 🚀 Filesystem, Architecture <a name = "deployment"></a>
### Microservice Approach
Filestructure follows [Digital Ocean](https://www.digitalocean.com) [___guidelines___](https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications#flask-the-minimalist-application-development-framework) for Large Flask projects.

### File Structure
```
.
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── controllers.py
│   │   ├── forms.py
│   │   └── models.py
│   ├── site
│   │   ├── __init__.py
│   │   ├── controllers.py
│   │   └── models.py
│   ├── spotify
│   │   ├── __init__.py
│   │   └── models.py
│   ├── static
│   └── templates
│       ├── 404.html
│       ├── auth
│       │   ├── signin.html
│       │   └── signup.html
│       └── site
│           ├── index_anonymous.html
│           └── index_signedin.html
├── app.db
├── config.py
├── docs
│   ├── 322 - Requirements Document.pdf
│   ├── File-Functions Map.png
│   └── Page Flow.png
├── requirements.txt
├── run.py
└── structure.txt
```

## ⛏️ Built Using <a name = "built_using"></a>
- [SQLAlchemy](https://www.sqlalchemy.org) - Database
- [Flask](http://flask.palletsprojects.com/en/1.1.x/) - Web Framework
- [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) - HTML Templating

## ✍️ Authors <a name = "authors"></a>
- [@bpoile](https://gitlab.eecs.wsu.edu/bpoile) - Benjamin Poile
- [@bsimon](https://gitlab.eecs.wsu.edu/bsimon) - Brevin Simon
- [@](https://gitlab.eecs.wsu.edu/) - Jiawei Liu
- [@](https://gitlab.eecs.wsu.edu/) - Leonard Brkanac

See also the list of [contributors](https://gitlab.eecs.wsu.edu/322-fall2019-termproject/team7/-/graphs/master) who participated in this project.

## 🎉 Documentation <a name = "documentation"></a>

See `./docs` directory for Assignment information and notes.
