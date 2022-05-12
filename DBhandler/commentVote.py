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
    commentId = data["commentId"]
    type = data["type"]
    time = datetime.datetime.now()

    insert_query = 'INSERT INTO commentVote (id,employeeId, commentId,type,time) ' \
                   'VALUES (?,?, ?,?,?)'
    fields = (id,employeeId, commentId ,type,time)
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
    commentId = data["commentId"]
    type = data["type"]
    time = data["time"]

    update_query = 'UPDATE commentVote SET employeeId=?, commentId=?,type=?,time=?' \
                   'WHERE id=?'
    fields = (employeeId, commentId,type,time , id)
    try:
        res = getCommentVoteByEmployeeComment(employeeId, commentId)
        if len(res)==0:
            response = "commentVote does not exist with this (employeeId, commentId)"
            return response
        if changeVote  and type ==res['type'] : # double upvotes ==> No vote  # double downvotes ==> No vote 
            delete(id)
            response = "commentVote deleted"
            return response
            
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "commentVote update successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - commentVote update Failed"
        return None

def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE commentVote WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "commentVote deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete commentVote"
        return None

def delete(username , commentId):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE commentVote '\
            'WHERE  commentVote.commentId IN'\
            '(SELECT comment.id from comment WHERE comment.id=?)'\
            'AND commentVote.employeeId IN'\
            '(SELECT emplyee.id from employee WHERE employee.username=?)'
            
    fields = (commentId,username, )

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "commentVote deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete commentVote"
        return None


def getCommentVoteByID(id):
    select_query = 'SELECT * FROM commentVote WHERE id=?'
    cursor.execute(select_query, (id,))
    commentVote = cursor.fetchall()
    return commentVote

def getCommentVoteByEmployeeComment(employeeID , commentID):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * commentVote INNER JOIN BY comment '\
            'ON  commentVote.commentId= comment.id INNER JOIN employee '\
            'ON commentVote.employeeId = employee.id'\
            'WHERE commentVote.employeeId=? AND commentVote.commentId=?'
            
    fields = (employeeID,commentID, )
    cursor.execute(select_query, fields)
    commentVote = cursor.fetchone()
    return commentVote

def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from commentVote")
    results = cursor.fetchall()
    close_db()
    return len(results)





