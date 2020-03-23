# Find my roommate

I learned flask from an udemy course. The course contains a course project, and I used this course project as a base, from which I built this basic framework for our cs316 project.

The current feature includes user registration (includes basic info for roommate matching), user login, update the account, CRUD (create, read, update, delete) posts for interacting with others in the finding roommate process.

To work on: integrate the matching algorithm, make a page that shows a list of users and their info. Of course, the front end team will make the web look more professional

How to run: 1: see the requirements.txt file, while contains a list of packages to be installed. Please refer to https://stackoverflow.com/questions/48787250/set-up-virtualenv-using-a-requirements-txt-generated-by-conda on how to create a virtual environment using the requirements.txt file. 2: After you have configured the virtual env and activated it, just run python app.py

A note: As of now, all the data is stored in data.sqlite, if you updated models.py, you need to make a migration for the database schema. First, delete the migrations file, then delete data.sqlite. Then run the following 3 commands in your shell respectively, flask db init, flask db migrate, flask db upgrade

Please feel free to shot me an message if you have any questions --Tommy


