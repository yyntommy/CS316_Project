# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from roommatefinder import db
from roommatefinder.models import User, BlogPost, House, UserLikes, Major, UserMajor
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

        if user is not None and user.check_password(form.password.data):

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
    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    class_entry_relations_major = get_dropdown_values_major()

    default_classes_major = sorted(class_entry_relations_major.keys())
    default_values_major = class_entry_relations_major[default_classes_major[0]]


    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            netid = current_user.netid
            pic = add_profile_pic(form.picture.data,netid)
            current_user.profile_image = pic

        current_user.name = form.name.data
        current_user.year = int(form.year.data)
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
        form.year.data = str(current_user.year)
        form.gender.data = current_user.gender
        form.smoking.data = current_user.smoking
        form.sleeping.data = current_user.sleeping
        form.waking.data = current_user.waking
        form.room_utility.data = current_user.room_utility
        form.on_campus.data = current_user.on_campus

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    print(profile_image)

    userlikes = db.session.query(UserLikes).filter(UserLikes.netid.like(current_user.netid)).all()
    usermajors = db.session.query(UserMajor).filter(UserMajor.netid.like(current_user.netid)).all()
    return render_template('account.html', profile_image=profile_image, form=form,
                            all_classes=default_classes, all_entries=default_values, userlikes=userlikes,
                            all_classes_major=default_classes_major, all_entries_major=default_values_major, usermajors=usermajors)

@users.route("/<netid>")
def user_posts(netid):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(netid=netid).first_or_404()
    userhouses = UserLikes.query.filter_by(netid=netid).all()
    houses = []
    for i in range(1, len(userhouses)+1):
        houses.append("Housing Preference " + str(i) + " : " + userhouses[i-1].building + ", " + userhouses[i-1].housename)
    usermajor = UserMajor.query.filter_by(netid=netid).all()
    majors = []
    for i in range(1, len(usermajor)+1):
        majors.append("Major: " + usermajor[i-1].school + ", " + usermajor[i-1].major)
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user,houses=houses,majors=majors)



def get_dropdown_values():


    #class_entry_relations = {'class1': ['val1', 'val2'],
                             #'class2': ['foo', 'bar', 'xyz']}
    class_entry_relations={}
    houses = db.session.query(House).all()
    for house in houses:
        temp = []
        aux_houses = db.session.query(House).filter(House.building.like(house.building)).all()
        for aux_house in aux_houses:
            temp.append(aux_house.name)
        class_entry_relations[house.building] = temp
    return class_entry_relations


@users.route('/_update_dropdown')
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@users.route('/_process_data')
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    userhouses = db.session.query(UserLikes)\
        .filter(UserLikes.netid == current_user.netid).all()
    temp = db.session.query(UserLikes)\
        .filter(UserLikes.netid == current_user.netid,
                UserLikes.housename == selected_entry,
                UserLikes.building == selected_class).all()
    if len(userhouses) < 5 and len(temp) == 0:
        userhouse = UserLikes(netid=current_user.netid,
                    housename=selected_entry,
                    building=selected_class)
        db.session.add(userhouse)
        db.session.commit()
    return jsonify(url=url_for('users.account'))

def get_dropdown_values_major():


    #class_entry_relations = {'class1': ['val1', 'val2'],
                             #'class2': ['foo', 'bar', 'xyz']}
    class_entry_relations={}
    majors = db.session.query(Major).all()
    for major in majors:
        temp = []
        aux_majors = db.session.query(Major).filter(Major.school.like(major.school)).all()
        for aux_major in aux_majors:
            temp.append(aux_major.name)
        class_entry_relations[major.school] = temp
    return class_entry_relations


@users.route('/_update_dropdown_major')
def update_dropdown_major():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown
    updated_values = get_dropdown_values_major()[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@users.route('/_process_data_major')
def process_data_major():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    usermajors = db.session.query(UserMajor)\
        .filter(UserMajor.netid == current_user.netid).all()
    if len(usermajors) == 0:
        usermajor = UserMajor(netid=current_user.netid,
                    major=selected_entry,
                    school=selected_class)
        db.session.add(usermajor)
        db.session.commit()
    return jsonify(url=url_for('users.account'))

# DELETE
@users.route('/<building>/<housename>/delete_house',methods=['GET','POST'])
def delete_house(building,housename):
    netid = current_user.netid
    house = db.session.query(UserLikes)\
        .filter(UserLikes.netid == current_user.netid,
                UserLikes.housename == housename,
                UserLikes.building == building)[0]
    db.session.delete(house)
    db.session.commit()
    flash('House Deleted')
    return redirect(url_for('users.account'))

@users.route('/delete_major',methods=['GET','POST'])
def delete_major():
    netid = current_user.netid
    major = db.session.query(UserMajor)\
        .filter(UserMajor.netid == current_user.netid)[0]
    db.session.delete(major)
    db.session.commit()
    flash('Major Deleted')
    return redirect(url_for('users.account'))
