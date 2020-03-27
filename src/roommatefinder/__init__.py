# puppycompanyblog/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy.event import listen
from roommatefinder.models import House, Major
from sqlalchemy import event, DDL

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'


############################
### DATABASE SETUP ##########
########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

#########################
# LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'



@event.listens_for(House.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(House(name='Avalon', building='Kilgo'))
    db.session.add(House(name='Banham', building='Edens'))
    db.session.commit()

@event.listens_for(Major.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(House(name='Dance', school='Trinity College of Arts and Sciences'))
    db.session.add(House(name='Economics', building='Trinity College of Arts and Sciences'))
    db.session.commit()



##################################################


from roommatefinder.core.views import core
from roommatefinder.users.views import users
from roommatefinder.blog_posts.views import blog_posts
from roommatefinder.error_pages.handlers import error_pages
from roommatefinder.match.views import match

app.register_blueprint(core)
app.register_blueprint(blog_posts)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(match)
