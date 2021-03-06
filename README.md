# Find My Roommate App

## Getting Started with the App

### Deployment

Deployed on Heroku: https://project-316.herokuapp.com/

### Deploying on Local

1. Pull the repo.
2. Install postgresql off the web--when making the default "postgres" account, assign the password to also be "postgres" unless you're willing to change the SQLALCHEMY_DATABASE_URI locally
3. Add the {path to}\PostgreSQL\12\bin directory to your path variables
4. Run the SQL Shell and enter in "create database data316proj;"
5. Open command prompt and navigate to your project folder. You should be in CS316_PROJECT. Then run the following commands:
    * psql -U postgres -h 127.0.0.1 -d data316proj -f ./create.sql
    * psql -U postgres -h 127.0.0.1 -d data316proj -f ./load.sql
    * psql -U postgres -h 127.0.0.1 -d data316proj -f ./load2.sql
6. The database should now exist locally on your system.
7. Install the requirements.txt packages.
8. Run the app through a CLI.

### Tips for Mac Users

There may be some issues downloading PostgreSQL onto your local machine if you have a Mac. One way to get around some of the issues is to download homebrew. See https://brew.sh on how to install homebrew.

After installing homebrew, run brew doctor to make sure everything will work correctly. Then, type brew install postgresql into your terminal. Add /usr/local/Cellar/postgresql/12.2/bin into your local directory by running the command sudo nano /etc/paths and adding it at the end of the paths list. Finally, run the commands above to create the database.

## Overview of Code Structure

The web is made with Flask, Jinja HTML, CSS, JavaScript(JQuery), raw SQL, and SQLAlchemy. We used blueprints from flask to break down the app into different components, such as users, core, blogposts, match, etc. The blueprints also took care of routing. We mainly used python for backend, and for the most of the time, the backend receives user inputs via wtforms. In term of the database, we used raw sql to create tables and load dataset. But for queries, we used SQLAlchemy, which is safe from injection attacks. Under our main source folder, we have a folder for each component, in which we have views.py (for backend) and forms.py (all of the wtforms). We also have a template folder that contains all of the html templates (frontend). On top of that, we have a file models.py (SQLAlchemy) which corresponds to our database model. 

## Current Implementation Limitations

The app currently has full functionality in regards to each of the current features. There are additional features that would have been fun to add--such as creating a  way for users to chat with each other outside of blog posts, but otherwise there are no limitations.
