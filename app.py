
from flask import Flask, request, url_for, redirect
from flask_cors import CORS
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
from DBhandler import ideaCategory as ideaCategory_DB
from DBhandler import comment as comment_DB
from DBhandler import commentVote as commentVote_DB
from DBhandler import committeeScoreHeader as committeeScoreHeader_DB
from DBhandler import committeeScoreDetail as committeeScoreDetail_DB
from DBhandler import evaluationCriteria as evaluationCriteria_DB
from DBhandler import award as award_DB
from DBhandler import tpi as tpi_DB


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


def get_personal_id(request):
    jwt_token = request.headers['Authorization'].split()[1]
    personal_id = tpi_DB.get(jwt_token)
    return personal_id


def current_user(request):
    jwt_token = request.headers['Authorization'].split()[1]
    personal_id = tpi_DB.get(jwt_token)
    user = employee_DB.get_by_personal_id(personal_id)
    return user


def is_admin(request):
    return current_user(request)['isAdmin'] == 1


@app.after_request
def refresh_expiring_jwts(response):
    try:
        response = update_jwt_if_expired(response)
        return response

    except (RuntimeError, KeyError):
        # this case is when there is not a valid JWT. Just return the original response
        return response


# ------ LOGIN/LOGOUT ------
@app.route('/login', methods=['POST'])
def login():
    personal_id = request.json['personal_id']
    user_exist = employee_DB.user_exist(personal_id)

    if not user_exist:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    password = request.json['password']
    correct_password = employee_DB.check_password(personal_id, password)

    if correct_password:
        access_token = create_access_token(identity=personal_id)

        data = {
            'jwt_token': access_token,
            'personal_id': personal_id,
        }

        tpi_DB.create(data)

        response = {"access_token": access_token}
        return response, STATUS_OK

    else:
        return {'message': WRONG_PASSWORD}, STATUS_BAD_REQUEST


@app.route('/logout', methods=['GET'])
@login_required()
def logout():
    # revoke_jwt()
    return {}, STATUS_OK


@app.route('/is_logged_in', methods=['GET'])
@login_required()
def is_logged_in():
    return {}, STATUS_OK


# ------ EMPLOYEE ENDPOINTS ------
@app.route('/register', methods=['POST'])
def signup():

    message = employee_DB.create(request.json)

    if message == USER_ALREADY_EXISTS:
        return {'message': USER_ALREADY_EXISTS}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    personal_id = request.json['personal_id']
    access_token = create_access_token(identity=personal_id)
    body = {'access_token': access_token}
    return body, STATUS_CREATED


@app.route('/get_user/<personal_id_>', methods=['GET'])
@login_required()
def get_user(personal_id_):

    personal_id = get_personal_id(request)
    permitted = personal_id == personal_id_ or is_admin(request)

    print(personal_id)
    print(personal_id_)

    if not permitted:
        return {}, STATUS_FORBIDDEN

    message = employee_DB.get_by_personal_id(personal_id)

    if type(message) is int:
        if message == NOT_FOUND:
            return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

        elif message == DB_ERROR:
            return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    data = message
    return data, STATUS_OK


@app.route('/update_user', methods=['POST'])
@login_required()
def update_user():

    personal_id = get_personal_id(request)
    permitted = personal_id == request.json['personal_id']

    if not permitted:
        return {}, STATUS_FORBIDDEN
    
    message = employee_DB.update(request.json)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/delete_user/<personal_id_>', methods=['DELETE'])
@login_required()
def delete_user(personal_id_):

    personal_id = get_personal_id(request)
    permitted = personal_id == personal_id_ or is_admin(request)

    if not permitted:
        return {}, STATUS_FORBIDDEN

    message = employee_DB.delete(personal_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/set_as_committeeMember/<personal_id_>', methods=['POST'])
@login_required()
def set_as_committeeMember(personal_id_):

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    employee_DB.set_as_committeeMember(personal_id_)


@app.route('/set_as_ordinaryMember/<personal_id_>', methods=['POST'])
@login_required()
def set_as_ordinaryMember(personal_id_):

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    employee_DB.set_as_ordinaryMember(personal_id_)


# ------ IDEA ENDPOINTS ------
@app.route('/create_idea', methods=['POST'])
@login_required()
def create_idea():
    message = idea_DB.create(request.json)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_CREATED


@app.route('/get_idea/<idea_id>')
# @login_required()
def get_idea(idea_id):
    message = idea_DB.getIdeaByID(idea_id)

    if type(message) is int:
        if message == NOT_FOUND:
            return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

        elif message == DB_ERROR:
            return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    data = message
    return data, STATUS_OK


@app.route('/get_idea_loggedIn/<idea_id>', methods=['POST'])
@login_required()
def get_idea_loggedIn(idea_id):
    personal_id = get_personal_id(request)
    message = idea_DB.getIdeaByID_loggedIn(idea_id, personal_id)

    if type(message) is int:
        if message == NOT_FOUND:
            return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

        elif message == DB_ERROR:
            return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    data = message
    return data, STATUS_OK


@app.route('/get_user_ideas/<personal_id>')
def get_user_ideas(personal_id):
    data = idea_DB.getIdeaByEmployeePersonalId(personal_id)
    return str(data)


@app.route('/get_all_ideas/<pagination_id>')
def get_ideas(pagination_id):
    ideas = idea_DB.getIdeas(pagination_id)
    return ideas, STATUS_OK


@app.route('/update_idea/<idea_id>', methods=['PATCH'])
@login_required()
def update_idea(idea_id):
    employeeId = current_user(request)['id']
    permitted = idea_DB.idea_is_for_user(employeeId, idea_id)
    if not permitted:
        return {}, STATUS_FORBIDDEN

    message = idea_DB.update(request.json, idea_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/delete_idea/<int:idea_id>', methods=['DELETE'])
@login_required()
def delete_idea(idea_id):
    employeeId = current_user(request)['id']
    permitted = idea_DB.idea_is_for_user(employeeId, idea_id)
    if not permitted:
        return {}, STATUS_FORBIDDEN

    message = idea_DB.delete(idea_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/change_idea_status/<int:idea_id>', methods=['UPDATE'])
@login_required()
def change_idea_status(idea_id):

    user = current_user(request)
    if not user['committeeMember']:
        return {}, STATUS_FORBIDDEN

    message = idea_DB.change_idea_status(request.json, idea_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


# ------ LIKE/DISLIKE IDEA ENDPOINTS ------
@app.route('/like_idea/<idea_id>', methods=['POST'])
@login_required()
def like_idea(idea_id):
    personal_id = get_personal_id(request)
    idea = dict(json.loads(idea_DB.getIdeaByID(idea_id)))
    
    not_permitted = idea['personal_id'] == personal_id
    if not_permitted:
        return {}, STATUS_FORBIDDEN

    employeeId = employee_DB.get_user_id(personal_id)
    message = idea_DB.like_idea(idea_id, employeeId)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/dislike_idea/<idea_id>', methods=['POST'])
@login_required()
def dislike_idea(idea_id):
    personal_id = get_personal_id(request)

    idea = dict(json.loads(idea_DB.getIdeaByID(idea_id)))

    not_permitted = idea['personal_id'] == personal_id
    if not_permitted:
        return {}, STATUS_FORBIDDEN

    employeeId = employee_DB.get_user_id(personal_id)
    message = idea_DB.dislike_idea(idea_id, employeeId)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


# ------ IDEA_CATEGORY ENDPOINTS ------
@app.route('/create_idea_cat', methods=['POST'])
@login_required()
def create_idea_cat():

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    message = ideaCategory_DB.create(request.json)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_CREATED


@app.route('/get_idea_cats')
@login_required()
def get_idea_cats():
    idea_categories = ideaCategory_DB.get_all_categories()
    return idea_categories


@app.route('/update_idea_cat/<int:idea_cat_id>', methods=['PATCH'])
@login_required()
def update_ideaCat(idea_cat_id):

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    message = ideaCategory_DB.update(request.json, idea_cat_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/delete_idea_cat_byId/<int:idea_cat_id>', methods=['DELETE'])
@login_required()
def delete_ideaCat_byId(idea_cat_id):

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    message = ideaCategory_DB.delete_by_id(idea_cat_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


# ------ COMMENT ENDPOINTS ------
@app.route('/create_comment', methods=['POST'])
@login_required()
def create_comment():

    message = comment_DB.create(request.json)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_CREATED


@app.route('/get_idea_comments/<idea_id>')
def get_idea_comments(idea_id):

    message = comment_DB.getCommentsByIdeaID(idea_id)

    if type(message) is int:
        if message == NOT_FOUND:
            return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

        elif message == DB_ERROR:
            return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    data = message
    return data, STATUS_OK


@app.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
@login_required()
def delete_comment(comment_id):

    employeeId = request.json['employeeId']
    permitted = comment_DB.comment_is_for_user(employeeId, comment_id) or is_admin(request)
    if not permitted:
        return {}, STATUS_FORBIDDEN

    message = comment_DB.delete(comment_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


# ------ COMMENT_VOTE ENDPOINTS ------
@app.route('/like_comment/<comment_id>', methods=['POST'])
@login_required()
def like_comment(comment_id):
    personal_id = get_personal_id(request)

    not_permitted = comment_DB.getCommentByID(comment_id)['personal_id'] == personal_id
    if not_permitted:
        return {}, STATUS_FORBIDDEN

    employeeId = employee_DB.get_user_id(personal_id)
    message = comment_DB.like_comment(comment_id, employeeId)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/dislike_comment/<comment_id>', methods=['POST'])
@login_required()
def dislike_comment(comment_id):
    personal_id = get_personal_id(request)

    not_permitted = comment_DB.getCommentByID(comment_id)['personal_id'] == personal_id
    if not_permitted:
        return {}, STATUS_FORBIDDEN

    employeeId = employee_DB.get_user_id(personal_id)
    message = comment_DB.dislike_comment(comment_id, employeeId)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK

# ----------------------------------------------------------

# ------- evaluationCriteria ENDPOINTS -------
@app.route('/get_ev_crits')
@login_required()
def get_ev_crits():
    ev_crits = evaluationCriteria_DB.get_all_ev_crits()
    return ev_crits


@app.route('/create_ev_crit', methods=['POST'])
@login_required()
def create_ev_crit():

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    message = evaluationCriteria_DB.create(request.json)

    if message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_CREATED


@app.route('/update_ev_crit/<int:ev_crit_id>', methods=['PATCH'])
@login_required()
def update_ev_crit(ev_crit_id):

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    message = evaluationCriteria_DB.update(request.json, ev_crit_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK


@app.route('/delete_ev_crit_byId/<int:ev_crit_id>', methods=['DELETE'])
@login_required()
def delete_ev_crit_byId(ev_crit_id):

    if not is_admin(request):
        return {}, STATUS_FORBIDDEN

    message = evaluationCriteria_DB.delete_by_id(ev_crit_id)

    if message == NOT_FOUND:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    elif message == DB_ERROR:
        return {'message': DB_ERROR}, STATUS_INTERNAL_SERVER_ERROR

    return {}, STATUS_OK
















# ------ TEST ENDPOINTS ------
@app.route('/test')
def test():
    data_dict = {
        'personal_id' : '1111',
        'password' : '11aa22',
    }

    message = employee_DB.create(data_dict)
    return {'message': message}, 200


@app.route('/test2')
def test2():
    personal_id = '1111'
    user_exist = employee_DB.user_exist(personal_id)

    if not user_exist:
        return {'message': NOT_FOUND}, STATUS_BAD_REQUEST

    password = '11aa22'
    correct_password = employee_DB.check_password(personal_id, password)

    if correct_password:
        access_token = create_access_token(identity=personal_id)
        tpi[access_token] = personal_id
        print(access_token)
        response = {"access_token": access_token}
        return response, STATUS_OK

    else:
        return {'message': WRONG_PASSWORD}, STATUS_BAD_REQUEST


@app.route('/test3/<access_token>')
# @login_required(optional=True)
def tets3(access_token):
    # personal_id = tpi[access_token]
    # print(personal_id)
    # user = employee_DB.get_by_personal_id(personal_id)
    return {'user': user}, 200



# ------ TESTING DB / EMPLOYEE ------
@app.route('/test_create')
def _1():
    data_dict = {
        'personal_id' : '2222',
        'password' : '2222',
        'committeeMember' : 0,
        'isAdmin' : 0,
    }

    message = employee_DB.create(data_dict)
    return str(message)


@app.route('/test_get/<personal_id>')
def _2(personal_id):
    data = employee_DB.get_by_personal_id(personal_id)
    return str(data)


@app.route('/test_get_all')
def _3():
    data = employee_DB.get_all_employees()
    return str(data)


@app.route('/test_update')
def _4():
    data_dict = {
        'firstName' : 'Alireza',
        'lastName' : 'Mohammadi',
        'personal_id' : '2222',
        'password' : '2222',
        'mobile' : '09129293929',
        'email' : 'm6@a.com',
        'committeeMember' : 0,
    }

    message = employee_DB.update(data_dict)
    return str(message)


@app.route('/test_delete/<id>')
def _5(id):
    message = employee_DB.delete(id)
    return str(message)


@app.route('/test_clear')
def _6():
    message = employee_DB.clear_table()
    return str(message)


# ------ TESTING DB / IDEA ------
@app.route('/test_create_idea')
def _i1():

    data_dict = {
        'personal_id' : 2222,
        'categoryId' : 3,
        'title' : 'some title 1',
        'text' : 'some text 1',
    }

    message = idea_DB.create(data_dict)
    return str(message)


@app.route('/test_get_idea_login/<id>')
def _i2(id,personal_id = 918273):
    # data = idea_DB.getIdeaByID_PersonalID(id,personal_id)
    # return str(data)
    pass

@app.route('/test_get_idea/<id>')
def _i8(id):

    data = idea_DB.getIdeaByID(id)
    return str(data)

@app.route('/test_clear_idea')
def _i3():

    data = idea_DB.clear_table()
    return str(data)


@app.route('/test_get_user_ideas/<personal_id>')
def _i4(personal_id):

    data = idea_DB.getIdeaByEmployeePersonalId(personal_id)
    return str(data)


@app.route('/test_get_all_ideas')
def _i5():

    data = idea_DB.get_all_ideas()
    return str(data)

@app.route('/test_clear_idea_ID/<id>')
def _i6(id):

    data = idea_DB.delete(id)
    return str(data)


@app.route('/test_clear_idea/<employeeId>/<idea_id>')
def _i7(employeeId,idea_id):

    data = idea_DB.idea_is_for_user(employeeId,idea_id)
    return str(data)

# ------ TESTING DB / IDEA VOTE------
@app.route('/test_create_upvote/')
def _iv1():
    data_dict = {
        'employeeId' : 2,
        'ideaId' : 1,
        'type' : 1,
    }

    message = ideaVote_DB.create(data_dict)
    return str(message)

@app.route('/test_update_upvote/')
def _iv2():
    data_dict = {
        'employeeId' : 2,
        'ideaId' : 1,
        'type' : 1,
    }

    message = ideaVote_DB.update(data_dict)
    return str(message)


@app.route('/test_create_downvote/')
def _iv3():
    data_dict = {
        'employeeId' : 2,
        'ideaId' : 1,
        'type' : 2,
    }

    message = ideaVote_DB.create(data_dict)
    return str(message)

@app.route('/test_update_downvote/')
def _iv4():
    data_dict = {
        'employeeId' : 2,
        'ideaId' : 1,
        'type' : 2,
    }

    message = ideaVote_DB.update(data_dict)
    return str(message)

# ------ TESTING DB / IDEA CATEGORY ------
@app.route('/test_create_idea_cats')
def _ic1():
    idea_cat1 = {'label': 'آموزشی' , 'value': 'آموزشی' }
    idea_cat2 = {'label': 'خدمات رفاهی','value': 'خدمات رفاهی' }
    idea_cat3 = {'label': 'خدمات انسانی','value': 'خدمات انسانی'}
    
    ideaCategory_DB.create(idea_cat1)
    ideaCategory_DB.create(idea_cat2)
    ideaCategory_DB.create(idea_cat3)
    return str(STATUS_CREATED)


@app.route('/test_clear_idea_cat_table')
def _ic2():
    message = ideaCategory_DB.clear_table()
    return message

# ------ TESTING DB / COMMENT ------

@app.route('/test_create_comment')
def _ico1():
    data_dict = {
        'personal_id' : 2222,
        'ideaId' : 1,
        'text' : 'some text nazar 2',
    }

    message = comment_DB.create(data_dict)
    return str(message)


@app.route('/test_get_idea_comments/<id>')
def _ico2(id):
    data = comment_DB.getCommentsByIdeaID(id)
    return str(data)

@app.route('/test_clear_comment_table')
def _ico3():
    message = comment_DB.clear_table()
    return message

# ------ TESTING DB / COMMENT_VOTE ------
@app.route('/test_create_commentVote_up')
def _icov1():
    data_dict = {
        'employeeId' : 1,
        'commentId' : 1,
        'type' : 1,
    }

    message = commentVote_DB.create(data_dict)
    return str(message)


@app.route('/test_create_commentVote_down')
def _icov2():
    data_dict = {
        'employeeId' : 1,
        'commentId' : 1,
        'type' : 2,
    }

    message = commentVote_DB.create(data_dict)
    return str(message)

@app.route('/test_clear_commentVote_table')
def _icov3():
    message = commentVote_DB.clear_table()
    return message


# ------ TESTING DB /  ------ Evaluation Criteria ------
@app.route('/test_create_ev_crit')
def _ec1():
    ev_crit0 = {
                'title': '---',
                'weight': 0
                }
    ev_crit1 = {
                'title': 'ev crit 1',
                'weight': 0.2
                }
    ev_crit2 = {
                'title': 'ev crit 2',
                'weight': 0.4,
                }
    ev_crit3 = {
                'title': 'ev crit 3',
                'weight': 0.4
                }
    
    evaluationCriteria_DB.create(ev_crit0)
    evaluationCriteria_DB.create(ev_crit1)
    evaluationCriteria_DB.create(ev_crit2)
    evaluationCriteria_DB.create(ev_crit3)
    return str(STATUS_CREATED)


# @app.route('/test_clear_idea_cat_table')
# def _ec2():
#     message = ideaCategory_DB.clear_table()
#     return message


# ----------------------------------------------------------

@app.errorhandler(STATUS_NOT_FOUND)
def not_found(error):
    return 'PAGE NOT FOUND!', STATUS_NOT_FOUND


if __name__ == "__main__":
    app.run(debug=True)
