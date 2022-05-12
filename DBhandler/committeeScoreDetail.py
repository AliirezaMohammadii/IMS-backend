import json
import re
import sys
import datetime
# windows
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend//DBhandler')
# macOs
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend/DBhandler')
sys.path.insert(0, '/Users/narges/Documents/GitHub/IMS-backend/DBhandler')

from db import *


def create(json):
    db = get_db()
    cursor = db.cursor()

    data = json.loads(json)
    id = get_table_size(cursor) +1
    committeeScoreHeaderId = data["committeeScoreHeaderId"]
    evaluationCriteriaId = data["evaluationCriteriaId"]
    score = data["score"]


    insert_query = 'INSERT INTO committeeScoreDetail (id,committeeScoreHeaderId, evaluationCriteriaId,score) ' \
                   'VALUES (?,?, ?,?)'
    fields = (id,committeeScoreHeaderId, evaluationCriteriaId,score)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "committeeScoreDetail insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - committeeScoreDetail insert Failed"
        return None



def update(json,id):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)
    
    committeeScoreHeaderId = data["committeeScoreHeaderId"]
    evaluationCriteriaId = data["evaluationCriteriaId"]
    score = data["score"]

    update_query = 'UPDATE committeeScoreDetail SET committeeScoreHeaderId=?, evaluationCriteriaId=?,score=?' \
                   'WHERE id=?'
    fields = (committeeScoreHeaderId, evaluationCriteriaId,score , id)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "committeeScoreDetail updated successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - committeeScoreDetail update Failed"
        return None


def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE committeeScoreDetail WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "committeeScoreDetail deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete committeeScoreDetail"
        return None


def getCommentByID(id):
    select_query = 'SELECT * FROM committeeScoreDetail WHERE id=?'
    cursor.execute(select_query, (id,))
    comment = cursor.fetchall()
    return comment



def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from comment")
    results = cursor.fetchall()
    close_db()
    return len(results)




