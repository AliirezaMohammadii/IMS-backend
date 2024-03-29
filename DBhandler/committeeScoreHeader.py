import json
import re
import sys

# windows
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend//DBhandler')
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend')
# macOs
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend/DBhandler')
sys.path.insert(0, '/Users/narges/Documents/GitHub/IMS-backend/DBhandler')
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend')
sys.path.insert(0, '/Users/narges/Documents/GitHub/IMS-backend')

from db import *
from Requirements import *
from DBhandler import employee as employee_DB
from DBhandler import idea as idea_DB
from DBhandler import committeeScoreDetail as committeeScoreDetail_DB


def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from committeeScoreHeader")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)


def create(employeeId, ideaId):
    db = get_db()
    cursor = db.cursor()


    id = get_table_size(cursor)+1
    # employeeId = employee_DB.get_user_id(data["personal_id"])
    # ideaId = data["ideaId"]

    time = solar_date_now()

    insert_query = 'INSERT INTO committeeScoreHeader (id,employeeId,ideaId,time) ' \
                   'VALUES (?,?,?,?)'

    fields = (id,employeeId,ideaId,time)

    # try:
    if getHeader(employeeId,ideaId, cursor) is not None:
        return SCORE_HEADER_ALREADY_EXISTS

    db = get_db()
    cursor = db.cursor()
    cursor.execute(insert_query, fields)
    db.commit()
    close_db()
    return MESSAGE_OK

    # except sqlite3.Error:
    close_db()
    return DB_ERROR


def update(data, id):
    db = get_db()
    cursor = db.cursor()

    employeeId = employee_DB.get_user_id(data["personal_id"])
    ideaId = data["ideaId"]
    time = data["time"]

    update_query = 'UPDATE committeeScoreHeader SET employeeId=?, ideaId=?,time=?' \
                   'WHERE id=?'
    fields = (employeeId, ideaId,time , id)
    try:

        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM committeeScoreHeader WHERE id=?'
    fields = (id,)

    try:
        cursor.execute(query, fields)
        db.commit()
        close_db()

        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def getHeaderByID(id):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * FROM committeeScoreHeader WHERE id=?'
    cursor.execute(select_query, (id,))
    comment = cursor.fetchall()

    close_db()

    return comment


def getIdeaScoreByPersonalID(ideaId, personal_id): # emtiaze har meyar ke yek fard dade be yek idea
    
    employee_id = employee_DB.get_user_id(personal_id)
    db = get_db()
    cursor = db.cursor()
    select_query = ' SELECT evaluationCriteria.id ,evaluationCriteria.title, ifnull(A.SC1,0) as SC FROM evaluationCriteria LEFT JOIN  ' \
                ' (SELECT evaluationCriteriaId, ifnull(committeeScoreDetail.score,0) as SC1  FROM  ' \
                'committeeScoreHeader  LEFT JOIN committeeScoreDetail ' \
                'ON committeeScoreHeader.id = committeeScoreDetail.committeeScoreHeaderId  ' \
                ' WHERE committeeScoreHeader.employeeId = ? and committeeScoreHeader.ideaId=? ) A ' \
                'ON evaluationCriteria.id = A.evaluationCriteriaId '

                    
                    
    cursor.execute(select_query, (employee_id,ideaId,))
    ideaScore = cursor.fetchall()
    close_db()
    return convert_to_json(ideaScore)


def getIdeaScore(ideaId):    # miangin emtiaze har meyar baraye yek idea
    db = get_db()
    cursor = db.cursor()
    
    select_query =  'SELECT evaluationCriteria.id , evaluationCriteria.title , AVG(ifnull(committeeScoreDetail.score,0)) score  FROM committeeScoreHeader  LEFT JOIN committeeScoreDetail '\
           'ON committeeScoreHeader.id = committeeScoreDetail.committeeScoreHeaderId  RIGHT JOIN JOIN evaluationCriteria '\
           'ON evaluationCriteria.id = committeeScoreDetail.evaluationCriteriaId '\
            ' WHERE committeeScoreHeader.ideaId=? '\
            'GROUP BY evaluationCriteria.id'
                    
                    
    cursor.execute(select_query, (ideaId,))
    ideasScores = cursor.fetchall()
    close_db()
    return convert_to_json(ideasScores)


def getHeader(employeeId,ideaId, cursor):
    select_query = 'SELECT * FROM committeeScoreHeader WHERE employeeId=? and ideaId=? '
    cursor.execute(select_query, (employeeId,ideaId,))
    header = cursor.fetchone()
    return header


def get_header_id(employeeId,ideaId, cursor):

    db = get_db()
    cursor = db.cursor()

    query = 'SELECT id FROM committeeScoreHeader WHERE employeeId=? and ideaId=? '

    try:
        cursor.execute(query, (employeeId,ideaId,))
        data = dict(cursor.fetchone())
        id = int(data['id'])
        close_db()
        return id
    
    except:
        close_db()
        return DB_ERROR


def checkChangeStatus(ideaId):
    db = get_db()
    cursor = db.cursor()

    query = 'SELECT count(*) FROM committeeScoreHeader WHERE committeeScoreHeader.ideaId=? '
    cursor.execute(query, (ideaId,))
    header = cursor.fetchone()[0]
    query = 'SELECT count(*) FROM employee WHERE committeeMember=1 '
    cursor.execute(query)
    committee = cursor.fetchone()[0]
    if header==committee:

        select_query = 'SELECT ifnull(totalScore.meanScore,0) meanScore  '\
                        'FROM idea '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id WHERE idea.id=? '
        
        cursor.execute(select_query, (ideaId,))
        score = cursor.fetchone()[0]
        if score > 6:
            data_dict = {
            'status' : 'Accepted',
            }
        else :
            data_dict = {
            'status' : 'Rejected',
            }

        idea_DB.change_idea_status(ideaId,data_dict)


def scoreAnIdea(personal_id , ideaId , evaluationCriteriaId , scoreOfCriteria):
    employeeId = employee_DB.get_user_id(personal_id)
    result = create(employeeId , ideaId)
    db = get_db()
    cursor = db.cursor()
    headerId = get_header_id(employeeId, ideaId, cursor=cursor)


    # detail:
    res = committeeScoreDetail_DB.create(headerId,evaluationCriteriaId,scoreOfCriteria)

    if res == SCORE_DETAIL_ALREADY_EXISTS:
        res = committeeScoreDetail_DB.update(headerId,evaluationCriteriaId,scoreOfCriteria)

    # print(convert_to_json(committeeScoreDetail_DB.getDetail_test(cursor)))
    checkChangeStatus(ideaId)
    return res

