#models.py
from roommatefinder import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True, nullable=False)
    netid = db.Column(db.String(64),unique=True,index=True, nullable=False)
    name = db.Column(db.String(64),nullable=False,index=True)
    gender = db.Column(db.String(1), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    smoking = db.Column(db.String(1), nullable=False)
    sleeping = db.Column(db.Integer, nullable=False)
    waking = db.Column(db.Integer, nullable=False)
    room_utility = db.Column(db.String(10), nullable=False)
    on_campus = db.Column(db.String(10), nullable=False)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self,netid,name,password,gender,year,smoking,sleeping,waking,room_utility,on_campus):
        self.netid = netid
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.gender = gender
        self.year = year
        self.smoking = smoking
        self.sleeping = sleeping
        self.waking = waking
        self.room_utility = room_utility
        self.on_campus = on_campus

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.netid}"


class House(db.Model):

    __tablename__ = 'house'

    name = db.Column('name', db.String(100), nullable=False, primary_key=True)
    building = db.Column('building', db.String(100),
                        nullable=False, primary_key=True)

    def __init__(self,name,building):
        self.name = name
        self.buidling = building


class Major(db.Model):

    __tablename__ = 'major'

    name = db.Column('name', db.String(100), nullable=False, primary_key=True)
    school = db.Column('school', db.String(100), nullable=False,
                primary_key=True)

    def __init__(self,name,school):
        self.name = name
        self.school = school


class UserLikes(db.Model):

    __tablename__ = 'userlikes'

    netid = db.Column('netid', db.String(6),
                    db.ForeignKey('users.netid'),
                    nullable=False, primary_key=True)
    housename = db.Column('housename', db.String(100),
                    db.ForeignKey('house.name'),
                    nullable=False, primary_key=True)
    building = db.Column('building', db.String(100),
                    db.ForeignKey('house.building'),
                    nullable=False, primary_key=True)

    def __init__(self,netid,housename,building):
        self.netid = netid
        self.housename = housename
        self.building = building

    def __repr__(self):
        return f"Likes {self.housename} in {self.building}"


class UserMajor(db.Model):

    __tablename__ = 'usermajor'

    netid = db.Column('netid', db.String(6),
                    db.ForeignKey('users.netid'),
                    nullable=False, primary_key=True)
    major = db.Column('major', db.String(100),
                    db.ForeignKey('major.name'),
                    nullable=False)
    school = db.Column('school', db.String(100),
                    db.ForeignKey('major.school'),
                    nullable=False)
    def __init__(self,netid,major,school):
        self.netid = netid
        self.major = major
        self.school = school


class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"
