# core/views.py
from roommatefinder.models import BlogPost
from flask import render_template,request,Blueprint

match = Blueprint('match',__name__)

@match.route('/')
def index():
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',blog_posts=blog_posts)

@match.route('/info')
def info():
    return render_template('info.html')


# import numpy as np
#
# from datetime import datetime, timedelta
#
#
#
#
#
# def cos_sim(a, b):
#
#     """Takes 2 vectors a, b and returns the cosine similarity according to the definition of the dot product
#
#     """
#
#     dot_product = np.dot(a, b)
#
#     norm_a = np.linalg.norm(a)
#
#     norm_b = np.linalg.norm(b)
#
#     return dot_product / (norm_a * norm_b)
#
#
#
#
#
# def wordvectorizer(vec1, vec2):
#
#     """Takes two lists of unique words and returns two numpy arrays of 0s and 1s indicating the number of words that are the same
#
#     """
#
#     total = list(set(vec1+vec2))
#
#     ret1 = [0 for x in total]
#
#     ret2 = [0 for x in total]
#
#     for i in range(len(total)):
#
#         if total[i] in vec1: ret1[i] = 1
#
#         if total[i] in vec2: ret2[i] = 1
#
#     return ret1, ret2
#
#
#
#
#
#
#
# def find_matches(netid, num):
#
#     """Takes a unique netid and finds the best num potential roommates for that user according to similarities in habits and preferences. Returns a list of tuples
#
#     """
#
#
#
#     # Retrieve relevant user and their relevant major/school
#
#     user = db.session.query(models.Users, models.UserMajor)\
#
#         .filter(models.Users.netid == netid).outerjoin(models.UserMajor).one()
#
#
#
#     # Get all matching genders, smoking habits, and on/off campus preferences, then join the potentials with their respective majors/schools
#
#     potentials = db.session.query(models.Users, models.UserMajor).filter(
#
#             models.Users.gender.like(user.gender),
#
#             models.Users.smoking.like(user.smoking),
# 
#             models.Users.on_campus.like(user.on_campus)
#
#         ).outerjoin(models.UserMajor).all()
#
#
#
#     # Create dictionary of netid:score, loop through all potentials to create score
#
#     for potential in potentials:
#
#
#
#         # Calculate major score partition 15%
#
#         if (not (user.major is None or potential.major is None)):
#
#             majorscore = cos_sim(wordvectorizer([user.major, user.school],[potential.major, potential.school]))
#
#         else: majorscore = 0
#
#
#
#         # Calculate year score partition 15%
#
#         yearscore = 1 - (np.linalg.norm(user.year - potential.year) / np.linalg.norm(2023-2020))
#
#
#
#         # Calculate waking/sleeping time score partition 40%
#
#         waking_diff_hrs = (user.waking - potential.waking).total_seconds() / 3600
#
#         sleeping_diff_hrs = (user.sleeping - potential.sleeping).total_seconds() / 3600
#
#         origin = np.array([0,0])
#
#         point = np.array([waking_diff_hrs, sleeping_diff_hrs])
#
#         highest = np.array([12,12])
#
#         timescore = 1 - (np.linalg.norm(origin-point) / np.linalg.norm(origin-highest))
#
#
#
#         # Calculate housing preference score partition 30%
#
#         user_pref = db.session.query(models.UserLikes)\
#
#             .filter(models.UserLikes.netid == user.netid).all()
#
#         potential_pref = db.session.query(models.UserLikes)\
#
#             .filter(models.UserLikes.netid == potential.netid).all()
#
#         if (not (user_pref.housename is None
#
#                     or potential_pref.housename is None)):
#
#             prefscore = cos_sim(wordvectorizer(user_pref.housename, potential_pref.housename))
#
#         else: prefscore = 1
#
#
#
#         overallscore = (.15 * majorscore + .15 * yearscore +
#
#                             .4 * timescore + .3 * prefscore)
#
#
#
#         score_tracker[potential.netid] = overallscore
#
#
#
#     # Sort dictionary to output best num roommates
#
#     new_tracker = {k:v for k,v in
#
#         sorted(score_tracker.items(), reverse=True, key=lambda item: item[1])}
#
#
#
#     # Create list of tuples
#
#     tuple_matches = []
#
#     index = 0
#
#     for netid,score in new_tracker.items():
#
#         if (index >= num): break
#
#         tuple_matches.append((netid, score))
#
#         index += 1
#
#
#
#     return tuple_matches
