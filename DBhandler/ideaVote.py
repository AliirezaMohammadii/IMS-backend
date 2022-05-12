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
    ideatId = data["commentId"]
    type = data["type"]
    time = datetime.datetime.now()

    insert_query = 'INSERT INTO ideaVote (id,employeeId, ideaId,type,time) ' \
                   'VALUES (?,?, ?,?,?)'
    fields = (id,employeeId, ideaId ,type,time)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "commentVote insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - commentVote insert Failed"
        return None



def update(json,id, changeVote= False): 
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)


    employeeId = data["employeeId"]
    ideaId = data["ideaId"]
    type = data["type"]
    time = data["time"]

    update_query = 'UPDATE ideaVote SET employeeId=?, ideaId=?,type=?,time=?' \
                   'WHERE id=?'
    fields = (employeeId, ideaId,type,time , id)
    try:
        res = getIdeaVoteByEmployeeIdea(employeeId, ideaId)
        if len(res)==0:
            response = "ideaVote does not exist with this (employeeId, ideaId)"
            return response
        if changeVote  and type ==res['type'] : # double upvotes ==> No vote  # double downvotes ==> No vote 
            delete(id)
            response = "ideaVote deleted"
            return response
            
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "ideaVote update successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - ideaVote update Failed"
        return None

def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE ideaVote WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "ideaVote deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete ideaVote"
        return None

def delete(username , ideaId):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE ideaVote '\
            'WHERE  ideaVote.ideaId IN'\
            '(SELECT idea.id from idea WHERE idea.id=?)'\
            'AND ideaVote.employeeId IN'\
            '(SELECT emplyee.id from employee WHERE employee.username=?)'
            
    fields = (ideaId,username, )

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "ideaVote deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete ideaVote"
        return None


def getIdeaVoteByID(id):
    select_query = 'SELECT * FROM ideaVote WHERE id=?'
    cursor.execute(select_query, (id,))
    ideaVote = cursor.fetchall()
    return ideaVote

def getIdeaVoteByEmployeeIdea(employeeID , ideaID):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * ideaVote INNER JOIN BY idea '\
            'ON  ideaVote.ideaId= idea.id INNER JOIN employee '\
            'ON ideaVote.employeeId = employee.id'\
            'WHERE ideaVote.employeeId=? AND ideaVote.ideaId=?'
            
    fields = (employeeID,ideaID, )
    cursor.execute(select_query, fields)
    ideaVote = cursor.fetchone()
    return ideaVote

def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from ideaVote")
    results = cursor.fetchall()
    close_db()
    return len(results)





