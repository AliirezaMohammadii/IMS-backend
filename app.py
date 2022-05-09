
from crypt import methods
from flask import Flask, make_response, request, session, url_for, redirect
from markupsafe import escape
import sys, os
from Requirements import *
from flask_cors import CORS

sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS')

from DBhandler import db
from DBhandler import employee as employee_DB
from DBhandler import idea as idea_DB
from DBhandler import ideaVote as ideaVote_DB
from DBhandler import comment as comment_DB
from DBhandler import commentVote as commentVote_DB
from DBhandler import committeeScoreHeader as committeeScoreHeader_DB
from DBhandler import committeeScoreDetail as committeeScoreDetail_DB
from DBhandler import evaluationCriteria as evaluationCriteria_DB
from DBhandler import award as award_DB


app = Flask(__name__)
cors = CORS(app)
app.secret_key = b'8a47ce117cfb2699cc021fcecd03773660d3ba0c369fd4252e4e6380b6f824b0'    # used for session
app.config['DEBUG'] = True
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
)
app.config.from_pyfile('config.py', silent=True)
db.init_app(app)


@app.route('/')
def index():
    if user_is_logged_in(session):
        return '', STATUS_OK
    return '', STATUS_UNAUTHORIZED

# ------ LOGIN/LOGOUT ------

@app.route('/login/', methods=['POST'])
def login():
    phone_number = request.json['phone_number']
    user_exist = employee_DB.user_exist(phone_number)

    if user_exist:
        session['personal_id'] = request.json['personal_id']
        return '', STATUS_OK

    else:
        return '', STATUS_BAD_REQUEST


@app.route('/logout/')
def logout():
    session.pop('personal_id', None)
    return '', STATUS_OK


# ------ EMPLOYEE ------

@app.route('/register/user/', methods=['POST'])
def signup():
    # app.logger.info('/register/user: %s', request.json)
    message = employee_DB.create(request.json)

    # CHECK MESSAGE FOR ERRORS

    session['personal_id'] = request.json['personal_id']      # login user
    return '', STATUS_CREATED


@app.route('/register/check/id/<personal_id>')
def check_duplicated_user(personal_id):
    personal_id_already_exists = employee_DB.user_exist(personal_id)

    if personal_id_already_exists:
        return '', STATUS_BAD_REQUEST

    return '', STATUS_OK


@app.route('/get_user_inf/')
def get_user():
    if user_is_logged_in(session):
        personal_id = session['personal_id']
        data = employee_DB.get_by_phone_number(personal_id)

        # CHECK DATA FOR ERRORS

        user_inf = {
            'personal_id'   : personal_id,
            'firstname'     : 'Alireza',
            'lastname'      : 'Mohammadi',
            # ...
        }
        return user_inf, STATUS_OK

    else:
        return '', STATUS_UNAUTHORIZED


# ------ IDEA ------

@app.route('/create_idea/', methods=['POST'])
def create_idea():
    if not user_is_logged_in(session):
        return '', STATUS_UNAUTHORIZED

    # message = idea_DB.create(request.json)

    # CHECK MESSAGE FOR ERRORS

    return '', STATUS_CREATED


# @app.route('/get_idea/<int:idea_id>')
# def get_idea(idea_id):
#     # data = idea_DB.get(idea_id)
#     pass


@app.route('/get_ideas/<pagination_id>/')
def ideas_timeline(pagination_id):
    if not user_is_logged_in(session):
        return '', STATUS_UNAUTHORIZED

    # ideas = idea_DB.get_ideas(pagination_id)     # send ideas in Timeline mode to backend.
    ideas = [
        'idea1',
        'idea2',
        'idea3',
        'idea4',
    ]
    return ideas, STATUS_OK


@app.route('/update_idea/', methods=['PATCH'])
def update_idea(idea_id):
    if not user_is_logged_in(session):
        return '', STATUS_UNAUTHORIZED

    permitted = True
    # permitted = idea_DB.idea_is_for_user(session['personal_id'], idea_id)
    if permitted:
        # message = idea_DB.update(request.json)

        # CHECK MESSAGE FOR ERRORS

        return '', STATUS_OK

    else:
        return '', STATUS_FORBIDDEN


@app.route('/delete_idea/<int:idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    if not user_is_logged_in(session):
        return '', STATUS_UNAUTHORIZED

    permitted = True
    # permitted = idea_DB.idea_is_for_user(session['personal_id'], idea_id)
    if permitted:
        # message = idea_DB.delete(idea_id)

        # CHECK MESSAGE FOR ERRORS

        return '', STATUS_OK

    else:
        return '', STATUS_FORBIDDEN


@app.route('/like_idea/<int:idea_id>', methods=['POST'])
def like_idea(idea_id):
    if not user_is_logged_in(session):
        return '', STATUS_UNAUTHORIZED

    # message = idea_DB.like_idea(idea_id)
    # example error: idea not found. For whenever request is made and sent directly by user, not web browser.

    return '', STATUS_OK


@app.route('/dislike_idea/<int:idea_id>', methods=['POST'])
def dislike_idea(idea_id):
    if not user_is_logged_in(session):
        return '', STATUS_UNAUTHORIZED

    # message = idea_DB.dislike_idea(idea_id)
    # example error: idea not found. For whenever request is made and sent directly by user, not web browser.

    return '', STATUS_OK


# .
# .
# .


# ---------------


# ---------------

@app.errorhandler(STATUS_NOT_FOUND)
def not_found(error):
    return 'PAGE NOT FOUND!', STATUS_NOT_FOUND