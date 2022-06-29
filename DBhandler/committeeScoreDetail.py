
import json
import re
import sys
from datetime import datetime

# windows
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend//DBhandler')
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend')
# macOs
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend/DBhandler')
sys.path.insert(0, '/Users/narges/Documents/GitHub/IMS-backend/DBhandler')
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend')
sys.path.insert(0, '/Users/narges/Documents/GitHub/IMS-backend')

from db import *


def create(committeeScoreHeaderId,evaluationCriteriaId,score ):
    db = get_db()
    cursor = db.cursor()

    data = json.loads(json)
    id = get_table_size(cursor) +1
    #committeeScoreHeaderId = data["committeeScoreHeaderId"]
    #evaluationCriteriaId = data["evaluationCriteriaId"]
    #score = data["score"]


    insert_query = 'INSERT INTO committeeScoreDetail (id,committeeScoreHeaderId, evaluationCriteriaId,score) ' \
                   'VALUES (?,?, ?,?)'
    fields = (id,committeeScoreHeaderId, evaluationCriteriaId,score)
    try:
        if getDetail(committeeScoreHeaderId,evaluationCriteriaId, cursor) is not None:
            return SCORE_DETAIL_ALREADY_EXISTS
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR



def update(committeeScoreHeaderId,evaluationCriteriaId,score ):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)
    
    #committeeScoreHeaderId = data["committeeScoreHeaderId"]
    #evaluationCriteriaId = data["evaluationCriteriaId"]
    #score = data["score"]

    update_query = 'UPDATE committeeScoreDetail SET score=?' \
                   'WHERE committeeScoreHeaderId=? and evaluationCriteriaId=? '
    fields = (score , committeeScoreHeaderId, evaluationCriteriaId)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def deleteByHeaderID(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM committeeScoreDetail WHERE committeeScoreHeader=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR

def deleteByID(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM committeeScoreDetail WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def getCommitteeScoreDetailByID(id):
    select_query = 'SELECT * FROM committeeScoreDetail WHERE id=?'
    cursor.execute(select_query, (id,))
    detail = cursor.fetchall()
    return detail



def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from committeeScoreDetail")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)




def getHeader(committeeScoreHeaderId,evaluationCriteriaId, cursor):
    select_query = 'SELECT * FROM committeeScoreDetail WHERE committeeScoreHeaderId=? and evaluationCriteriaId=? '
    cursor.execute(select_query, (committeeScoreHeaderId,evaluationCriteriaId,))
    detail = cursor.fetchone()
    return detail