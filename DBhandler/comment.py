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
    text = data["text"]
    time = datetime.datetime.now()

    insert_query = 'INSERT INTO comment (id,employeeId, ideaId,text,time) ' \
                   'VALUES (?,?, ?,?,?)'
    fields = (id,employeeId, ideaId,text,time)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "comment insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - comment insert Failed"
        return None



def update(json,id):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)


    employeeId = data["employeeId"]
    ideaId = data["ideaId"]
    text = data["text"]
    time = data["time"]

    update_query = 'UPDATE comment SET employeeId=?, ideaId=?,text=?,time=?' \
                   'WHERE id=?'
    fields = (employeeId, ideaId,text,time , id)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "comment update successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - comment update Failed"
        return None


def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE comment WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "comment deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to comment idea"
        return None


def getCommentByID(id):
    select_query = 'SELECT * FROM comment WHERE id=?'
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


def getCommentsByIdeaID(id):  # Get an idea comments with votes for each comment and information about the employee who submitted the comment
    select_query = 'SELECT *,(SELECT COUNT(*) FROM commentVote where comment.id=commentVote.commentId and commentVote.type=1) as upVotes, (SELECT COUNT(*) FROM commentVote where comment.id=commentVote.commentId and commentVote.type=0) as downVotes '\
                    'FROM idea INNER JOIN BY comment  ' \
                    'ON idea.id = comment.ideaId  ' \
                    'INNER JOIN BY employee  ' \
                    'ON employee.id = comment.employeeId  ' \
                    'WHERE idea.id=? ' \
                    'ORDER BY comment.time DESC'
    cursor.execute(select_query, (id,))
    commentsWithVotes = cursor.fetchall()
    return commentsWithVotes

