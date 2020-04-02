# core/views.py
from roommatefinder import db
from roommatefinder.models import User, UserMajor, UserLikes
from flask import render_template,request,Blueprint
from flask_login import current_user
import numpy as np
from datetime import datetime, timedelta


match = Blueprint('match',__name__)

# @match.route('/match')
# def index():
#     page = request.args.get('page',1,type=int)
#     users = User.query.order_by(User.netid.desc()).paginate(page=page,per_page=5)
#     return render_template('match.html',users=users, similarity=5)

@match.route('/match')
def index():

    # NOTE: THIS DOESN'T ACTUALLY WORK AS FAR AS DISPLAYING MATCHES GOES BECAUSE IT DISPLAYS THE MATCHES OUT OF ORDER AND ALSO JUST DISPLAYS A LIST OF THE SIMILARITIES IN THE SIMILARITIES AREA

    page = request.args.get('page',1,type=int)
    users = find_matches(current_user.netid, 100)
    return render_template('match.html',users=users)


def getKey(item):
    return item[2]

def cos_sim(a, b):
    """Takes 2 vectors a, b and returns the cosine similarity according to the definition of the dot product
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


def wordvectorizer(vec1, vec2):
    """Takes two lists of unique words and returns two numpy arrays of 0s and 1s indicating the number of words that are the same
    """
    total = list(set(vec1+vec2))
    ret1 = [0 for x in total]
    ret2 = [0 for x in total]
    for i in range(len(total)):
        if total[i] in vec1: ret1[i] = 1
        if total[i] in vec2: ret2[i] = 1
    return ret1, ret2



def find_matches(netid, num):
    """Takes a unique netid and finds the best num potential roommates for that user according to similarities in habits and preferences. Returns a list of tuples
    """

    # Retrieve relevant user and their relevant major/school
    user = db.session.query(User, UserMajor)\
        .filter(User.netid == netid).outerjoin(UserMajor).all()

    # Get all matching genders, smoking habits, and on/off campus preferences, then join the potentials with their respective majors/schools
    potentials = db.session.query(User, UserMajor).filter(
            User.gender.like(user[0][0].gender),
            User.smoking.like(user[0][0].smoking),
            User.on_campus.like(user[0][0].on_campus),
            User.netid != netid
        ).outerjoin(UserMajor).all()

    # Create dictionary of netid:score, loop through all potentials to create score
    score_tracker = []
    for potential in potentials:

        # Calculate major score partition 15%
        if (not (user[0][1] is None or potential[1] is None)):
            a, b = wordvectorizer([user[0][1].major, user[0][1].school],[potential[1].major, potential[1].school])
            majorscore = cos_sim(a, b)
        else: majorscore = 0

        # Calculate year score partition 15%
        unum = int(user[0][0].year)
        pnum = int(potential[0].year)
        yearscore = 1 - (np.linalg.norm(unum - pnum) / np.linalg.norm(2023-2020))

        # Calculate waking/sleeping time score partition 40%
        nd = datetime(1,1,1)
        wtimeu = datetime.combine(nd, user[0][0].waking)
        wtimep = datetime.combine(nd, potential[0].waking)
        stimeu = datetime.combine(nd, user[0][0].sleeping)
        stimep = datetime.combine(nd, potential[0].sleeping)
        waking_diff_hrs = (wtimeu - wtimep).total_seconds() / 3600
        sleeping_diff_hrs = (stimeu - stimep).total_seconds() / 3600
        origin = np.array([0,0])
        point = np.array([waking_diff_hrs, sleeping_diff_hrs])
        highest = np.array([12,12])
        timescore = 1 - (np.linalg.norm(origin-point) / np.linalg.norm(origin-highest))

        # Calculate housing preference score partition 30%
        user_pref = db.session.query(UserLikes)\
            .filter(UserLikes.netid == user[0][0].netid).all()
        potential_pref = db.session.query(UserLikes)\
            .filter(UserLikes.netid == potential[0].netid).all()
        if (not (len(user_pref)==0 or len(potential_pref)==0) ):
            a, b = wordvectorizer(user_pref, potential_pref)
            prefscore = cos_sim()
        else: prefscore = 1

        overallscore = (.15 * majorscore + .15 * yearscore +
                            .4 * timescore + .3 * prefscore)

        score_tracker.append((potential[0].netid, potential[0].name, overallscore))

    tuple_matches = []
    index = 0
    for item in score_tracker:
        if (index >= num): break
        tuple_matches.append(item)
        index += 1

    tuple_matches = sorted(tuple_matches, reverse=True, key=getKey)
    return tuple_matches
