# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from roommatefinder import db
from roommatefinder.models import User, BlogPost
from roommatefinder.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from roommatefinder.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(netid=form.netid.data,
                    name=form.name.data,
                    password=form.password.data,
                    gender=form.gender.data,
                    year=form.year.data,
                    smoking=form.smoking.data,
                    sleeping=form.sleeping.data,
                    waking=form.waking.data,
                    room_utility=form.room_utility.data,
                    on_campus=form.on_campus.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)



# login
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(netid=form.netid.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# account (update UserForm)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            netid = current_user.netid
            pic = add_profile_pic(form.picture.data,netid)
            current_user.profile_image = pic

        current_user.name = form.name.data
        current_user.gender = form.gender.data
        current_user.smoking = form.smoking.data
        current_user.sleeping = form.sleeping.data
        current_user.waking = form.waking.data
        current_user.room_utility = form.room_utility.data
        current_user.on_campus = form.on_campus.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.gender.data = current_user.gender
        form.smoking.data = current_user.smoking
        form.sleeping.data = current_user.sleeping
        form.waking.data = current_user.waking
        form.room_utility.data = current_user.room_utility
        form.on_campus.data = current_user.on_campus

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

@users.route("/<netid>")
def user_posts(netid):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(netid=netid).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)













# user's list of Blog posts