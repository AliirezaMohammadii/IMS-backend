
from flask import Flask, request, url_for, redirect
from flask_cors import CORS
from markupsafe import escape
import sys, os, time
import json
from datetime import datetime, timedelta, timezone

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


# ------ LOGIN/LOGOUT ------
@app.route('/login', methods=['POST'])
def login():
    personal_id = request.json['id']
    user_exist = employee_DB.user_exist(personal_id)

    if not user_exist:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    password = request.json['password']
    correct_password = employee_DB.check_password(personal_id, password)

    if correct_password:
        access_token = create_access_token(identity=personal_id)
        response = {"access_token": access_token}
        return response, STATUS_OK

    else:
        return {'message': WRONG_PASSWORD}, STATUS_BAD_REQUEST


@app.route('/logout')
@login_required()
def logout():
    revoke_jwt()
    return {}, STATUS_OK


# ------ EMPLOYEE ENDPOINTS ------
@app.route('/register', methods=['POST'])
def signup():

    message = employee_DB.create(request.json)

    if message == USER_ALREADY_EXISTS:
        return {'message': USER_ALREADY_EXISTS}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_BAD_REQUEST

    personal_id = request.json['id']
    access_token = create_access_token(identity=personal_id)
    body = {'access_token': access_token}
    return body, STATUS_CREATED


@app.route('/get_user/<personal_id>', methods=['GET'])
@login_required()
def get_user(personal_id):

    # TODO
    # TO CHECK ACCESSIBILITY PERMISSION
    # CHECK IF THE ONE WHO IS USING THIS ENDPOINT, IS THE CURRENT USER DELETUNG HIS ACCOUNT, OR IS THE ADMIN.
    # OTHER WISE, DON'T PERMIT.
    # PREREQ.: ADDING JWT TOKEN TO TABLE.

    message = employee_DB.get_by_personal_id(personal_id)
    if type(message) is int:
        if message == NOT_FOUND:
            return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

        elif message == DB_ERROR:
            return {'message': DB_ERROR}, STATUS_BAD_REQUEST

    data = message
    return data, STATUS_OK


@app.route('/update_user', methods=['PATCH'])
@login_required()
def update_user():

    # TODO
    # TO CHECK ACCESSIBILITY PERMISSION
    # CHECK IF THE ONE WHO IS USING THIS ENDPOINT, IS THE CURRENT USER DELETUNG HIS ACCOUNT.
    # OTHER WISE, DON'T PERMIT.
    # PREREQ.: ADDING JWT TOKEN TO TABLE.

    message = employee_DB.update(request.json)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_BAD_REQUEST

    return {}, STATUS_OK


@app.route('/delete_user/<personal_id>', methods=['DELETE'])
@login_required()
def delete_user(personal_id):

    # TODO
    # TO CHECK ACCESSIBILITY PERMISSION
    # CHECK IF THE ONE WHO IS USING THIS ENDPOINT, IS THE CURRENT USER DELETUNG HIS ACCOUNT, OR IS THE ADMIN.
    # OTHER WISE, DON'T PERMIT.
    # PREREQ.: ADDING JWT TOKEN TO TABLE.

    message = employee_DB.delete(personal_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_BAD_REQUEST

    return {}, STATUS_OK


# ------ IDEA ENDPOINTS ------
@app.route('/create_idea', methods=['POST'])
@login_required()
def create_idea():

    error = idea_DB.create(request.json)

    # CHECK MESSAGE FOR ERRORS

    return {}, STATUS_CREATED


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
        return {'error': NOT_FOUND}, STATUS_BAD_REQUEST



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


# ----------------------------------------------------------

# ------ TEST ENDPOINTS ------
@app.route('/test')
def test():
    return {}


@app.route('/test2')
@login_required()
def test2():
    return {'message': 'user is logged in'}, STATUS_OK


@app.route('/test3')
@login_required(optional=True)
def tets3():
    get_identity = get_jwt_identity()
    if get_identity:
        return {'identity': get_identity}, STATUS_OK

    else:
        return {'identity': 'Anonymous'}, STATUS_OK


# ------ TESTING DB / EMPLOYEE ------
@app.route('/test_create')
def _1():
    data_dict = {
        'firstName' : 'Ali',
        'lastName' : 'Mo',
        'personal_id' : '1234',
        'password' : '1111',
        'mobile' : '09121111111',
        'email' : 'a@b.com',
        'committeeMember' : 0,
    }

    data_json = json.dumps(data_dict)
    message = employee_DB.create(data_json)
    return 'message'


@app.route('/test_get/<id>')
def _2(id):
    data = employee_DB.get_by_personal_id(id)
    return data


@app.route('/test_get_all')
def _3():
    data = employee_DB.get_all_employees()
    return data


@app.route('/test_update')
def _4():
    data_dict = {
        'firstName' : 'Alireza',
        'lastName' : 'Mohammadi',
        'personal_id' : '9999',
        'password' : '2222',
        'mobile' : '09121111111',
        'email' : 'a@b.com',
        'committeeMember' : 0,
    }

    data_json = json.dumps(data_dict)
    message = employee_DB.update(data_json)
    return message


@app.route('/test_delete/<id>')
def _5(id):
    message = employee_DB.delete(id)
    return message


@app.route('/test_clear')
def _6():
    message = employee_DB.clear_table()
    return message


# ------ TESTING DB / EMPLOYEE ------

@app.route('/test_create_i')
def _i1():
    data_dict = {
        'employeeId' : 9999,
        'categoryId' : 12,
        'title' : 'some title',
        'text' : 'some text',
        'costReduction' : 2000,
        'time' : 0,
        'status' : None,
    }

    data_json = json.dumps(data_dict)
    message = employee_DB.create(data_json)
    return 'message'

# ----------------------------------------------------------

@app.errorhandler(STATUS_NOT_FOUND)
def not_found(error):
    return 'PAGE NOT FOUND!', STATUS_NOT_FOUND


if __name__ == "__main__":
    app.run(debug=True)