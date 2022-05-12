import json
import re
import sys

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
    title = data["title"]
    weight = data["weight"]
    insert_query = 'INSERT INTO evaluationCriteria (id, title, weight) ' \
                   'VALUES (?,?, ?)'
    fields = (title, weight)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "evaluationCriteria insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - evaluationCriteria insert Failed"
        return None



def update(json,id):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)
    title = data["title"]
    weight = data["weight"]
    update_query = 'UPDATE evaluationCriteria SET title =?, weight =?' \
                   'WHERE id=?'
    fields = (title, weight , id)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "evaluationCriteria insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - evaluationCriteria insert Failed"
        return None



def getEvaluationCriteriaByID(id):
    select_query = 'SELECT * FROM evaluationCriteria WHERE id=?'
    cursor.execute(select_query, (id,))
    evaluationCriteria = cursor.fetchall()
    return evaluationCriteria



def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from evaluationCriteria")
    results = cursor.fetchall()
    close_db()
    return len(results)