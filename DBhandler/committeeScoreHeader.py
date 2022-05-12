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
    employeeId = data["employeeId"]
    ideaId = data["ideaId"]

    time = datetime.datetime.now()

    insert_query = 'INSERT INTO committeeScoreHeader (id,employeeId, ideaId,time) ' \
                   'VALUES (?,?, ?,?)'
    fields = (id,employeeId, ideaId,time)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "committeeScoreHeader insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - committeeScoreHeader insert Failed"
        return None



def update(json,id):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)


    employeeId = data["employeeId"]
    ideaId = data["ideaId"]
    text = data["text"]
    time = data["time"]

    update_query = 'UPDATE committeeScoreHeader SET employeeId=?, ideaId=?,time=?' \
                   'WHERE id=?'
    fields = (employeeId, ideaId,time , id)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "committeeScoreHeader updated successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - committeeScoreHeader update Failed"
        return None


def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE committeeScoreHeader WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "committeeScoreHeader deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to comment idea"
        return None


def getCommentByID(id):
    select_query = 'SELECT * FROM committeeScoreHeader WHERE id=?'
    cursor.execute(select_query, (id,))
    comment = cursor.fetchall()
    return comment



def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from committeeScoreHeader")
    results = cursor.fetchall()
    close_db()
    return len(results)




def getIdeaScore(ideaId): # get score of an idea
    
    select_query = 'SELECT h.ideaId, idea.title,sum(score*weight)/count(h.id) score FROM idea, committeeScoreHeader  h, committeeScoreDetail d,evaluationCriteria e where  h.id = d.committeeScoreHeaderId'\
                    'and e.id = d.evaluationCriteriaId and idea.id=h.ideaId' \
                    'group by h.ideaId  '\
                    'WHERE idea.id=? ' 
                    
    cursor.execute(select_query, (id,))
    ideaScore = cursor.fetchall()
    return ideaScore

def getIdeasScores():   # get all ideas + scores
    
    select_query = 'SELECT h.ideaId,idea.* , sum(score*weight)/count(h.id) score FROM idea , committeeScoreHeader  h, committeeScoreDetail d,evaluationCriteria e where  h.id = d.committeeScoreHeaderId'\
                    'and e.id = d.evaluationCriteriaId and idea.id=h.ideaId'\
                    'group by h.ideaId  '
                    
                    
    cursor.execute(select_query)
    ideasScores = cursor.fetchall()
    return ideasScores








