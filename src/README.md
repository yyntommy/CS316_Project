# Find my roommate

Updated README.md as of 4/1/20:

The matching algorithm has been integrated and works with the current database, now it just needs to have an actual page in the app.

IMPORTANT: The requirements.txt has been updated, so make sure to update your virtual env. Also, we've moved away from SQLite and are now using PostgreSQL. To make sure your app can run, do the following (this assumes you're using Windows, but the process is similar on other OS'):

1. Pull changes, and make sure the migrations directory and data.sqlite file are deleted.
2. Install postgresql off the web--when making the default "postgres" account, assign the password to also be "postgres" unless you're willing to change the SQLALCHEMY_DATABASE_URI locally
3. Add the {path to}\PostgreSQL\12\bin directory to your path variables
4. Run the SQL Shell and enter in "create database data316proj"
5. Open command prompt and navigate to your project folder. You should be in CS316_PROJECT. Then run the following commands:
    * psql -U postgres -h 127.0.0.1 -d data316proj -f ./create.sql
    * psql -U postgres -h 127.0.0.1 -d data316proj -f ./load.sql
6. The database should now exist locally on your system. You can run the app without doing any migrations.

If you have any difficulties, just text me or something --Niko


3/22/20:

I learned flask from an udemy course. The course contains a course project, and I used this course project as a base, from which I built this basic framework for our cs316 project.

The current feature includes user registration (includes basic info for roommate matching), user login, update the account, CRUD (create, read, update, delete) posts for interacting with others in the finding roommate process.

To work on: integrate the matching algorithm, make a page that shows a list of users and their info. Of course, the front end team will make the web look more professional

How to run: 1: see the requirements.txt file, while contains a list of packages to be installed. Please refer to https://stackoverflow.com/questions/48787250/set-up-virtualenv-using-a-requirements-txt-generated-by-conda on how to create a virtual environment using the requirements.txt file. 2: After you have configured the virtual env and activated it, just run python app.py

A note: As of now, all the data is stored in data.sqlite, if you updated models.py, you need to make a migration for the database schema. First, delete the migrations file, then delete data.sqlite. Then run the following 3 commands in your shell respectively, flask db init, flask db migrate, flask db upgrade

Please feel free to shot me an message if you have any questions --Tommy
