
from flask import Flask, make_response, request, session, url_for, redirect
from flask_cors import CORS
from markupsafe import escape
import sys, os, time
import json
from datetime import datetime, timedelta, timezone

from numpy import identity
from Requirements import *
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended import jwt_required as login_required

# windows
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend')
# macOs
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend')

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
    DATABASE=os.path.join(app.root_path + '/db_files', 'app.sqlite'),
)
app.config.from_pyfile('config.py', silent=True)
jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
db.init_app(app)


@app.after_request
def refresh_expiring_jwts(response):
    try:
        response = update_jwt_if_expired(response)
        return response

    except (RuntimeError, KeyError):
        # this case is when there is not a valid JWT. Just return the original respone
        return response


@app.route('/test')
@login_required()
def test():
    return {'message': 'user is logged in'}, STATUS_OK


@app.route('/test2')
@login_required(optional=True)
def tets2():
    get_identity = get_jwt_identity()
    if get_identity:
        return {'identity': get_identity}, STATUS_OK

    else:
        return {'identity': 'Anonymous'}, STATUS_OK


@app.route('/test3')
def test3():
    data_dict = {
        'firstName' : 'Ali',
        'lastName' : 'Mo',
        'username' : '1234',
        'password' : '1111',
        'mobile' : '09121111111',
        'email' : 'a@b.com',
        'committeeMember' : True,
    }

    data_json = json.dumps(data_dict)

    error = employee_DB.create(data_json)

    return error


@app.route('/test4/<id>')
def test4(id):

    data = employee_DB.get_by_personal_id(id)

    log(data)
    return data

# ------ LOGIN/LOGOUT ------

@app.route('/login', methods=['POST'])
def login():
    personal_id = request.json['id']
    # user_exist = employee_DB.user_exist(personal_id)
    user_exist = True

    if user_exist:

        password = request.json['password']
        # correct_password = employee_DB.check_password(personal_id, password)
        correct_password = True

        if correct_password:
            access_token = create_access_token(identity=personal_id)
            response = {"access_token": access_token}
            return response

        else:
            return {'message', WRONG_PASSWORD}, STATUS_BAD_REQUEST

    else:
        return {'message', USER_NOT_FOUND}, STATUS_BAD_REQUEST


@app.route('/logout')
def logout():
    revoke_jwt()
    return {}, STATUS_OK


# ------ EMPLOYEE ------

@app.route('/register/user', methods=['POST'])
def signup():
    
    error = ''
    # error = employee_DB.create(request.json)

    # if error != '':
    #     if error == ...:
    #         ...
    #     elif error == ...:
    #         ...

    personal_id = request.json['id']
    access_token = create_access_token(identity=personal_id)
    body = {'access_token': access_token}
    log(access_token)
    # log(request)
    # log(request.json)
    return body, STATUS_CREATED


# @app.route('/register/check/id/<personal_id>')
# def check_duplicated_user(personal_id):
#     # personal_id_already_exists = employee_DB.user_exist(personal_id)
#     personal_id_already_exists = ''

#     if personal_id_already_exists:
#         return '', STATUS_BAD_REQUEST

#     return '', STATUS_OK


# @app.route('/get_user_inf')
# def get_user():
#     if user_is_logged_in(session):
#         personal_id = session['personal_id']
#         # data = employee_DB.get_by_phone_number(personal_id)
#         data = ''

#         # CHECK DATA FOR ERRORS

#         user_inf = {
#             'personal_id'   : personal_id,
#             'firstname'     : 'Alireza',
#             'lastname'      : 'Mohammadi',
#             # ...
#         }
#         return user_inf, STATUS_OK

#     else:
#         return '', STATUS_UNAUTHORIZED


# ------ IDEA ------

@app.route('/create_idea', methods=['POST'])
@login_required()
def create_idea():

    error = ''
    # error = idea_DB.create(request.json)

    # CHECK MESSAGE FOR ERRORS

    return '', STATUS_CREATED


# @app.route('/get_idea/<int:idea_id>')
# def get_idea(idea_id):
#     # data = idea_DB.get(idea_id)
#     pass


@app.route('/get_idea/<int:idea_id>')
@login_required()
def get_idea(idea_id):

    data = ''
    # data = idea_DB.get_idea(idea_id)

    if type(data) == dict:
        return data

    else:   # some error is returned
        return {'error': IDEA_NOT_FOUND}, STATUS_BAD_REQUEST



@app.route('/get_ideas/<pagination_id>')
def get_ideas(pagination_id):

    # ideas = idea_DB.get_ideas(pagination_id)     # send ideas in Timeline mode to backend.
    ideas = [
        {
            'id'            : 0,    
            'employeeId'    : 1,
            'categoryId'    : 1,
            'title'         : 'Title 1',
            'text'          : 'Text 1',
            'costReduction' : 10,    
            'time'          : 0,
            'status'        : 'pending'
        },
        {
            'id'            : 1,    
            'employeeId'    : 6,
            'categoryId'    : 12,
            'title'         : 'Title 2',
            'text'          : 'Text 2',
            'costReduction' : 55,    
            'time'          : 1,
            'status'        : 'rejected'
        },
    ]

    return ideas, STATUS_OK


@app.route('/update_idea', methods=['PATCH'])
@login_required()
def update_idea(idea_id):

    permitted = True
    # permitted = idea_DB.idea_is_for_user(..., idea_id)
    if permitted:
        # message = idea_DB.update(request.json)

        # CHECK MESSAGE FOR ERRORS

        return '', STATUS_OK

    else:
        return '', STATUS_FORBIDDEN


@app.route('/delete_idea/<int:idea_id>', methods=['DELETE'])
@login_required()
def delete_idea(idea_id):

    permitted = True
    # permitted = idea_DB.idea_is_for_user(session['personal_id'], idea_id)
    if permitted:
        # message = idea_DB.delete(idea_id)

        # CHECK MESSAGE FOR ERRORS
        return '', STATUS_OK

    else:
        return '', STATUS_FORBIDDEN


@app.route('/like_idea/<int:idea_id>', methods=['POST'])
@login_required()
def like_idea(idea_id):

    # message = idea_DB.like_idea(idea_id)
    # example error: idea not found. For whenever request is made and sent directly by user, not web browser.

    return '', STATUS_OK


@app.route('/dislike_idea/<int:idea_id>', methods=['POST'])
@login_required()
def dislike_idea(idea_id):

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