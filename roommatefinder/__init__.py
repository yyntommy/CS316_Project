# puppycompanyblog/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import request


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'


############################
### DATABASE SETUP ##########
########################
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

db = SQLAlchemy(app)
Migrate(app,db)

#########################
# LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'






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
