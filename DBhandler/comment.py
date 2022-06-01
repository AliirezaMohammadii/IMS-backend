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


def create(data):
    db = get_db()
    cursor = db.cursor()

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



def update(data):
    db = get_db()
    cursor = db.cursor()
    

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
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE comment WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def getCommentByID(id):
    select_query = 'SELECT * FROM comment WHERE id=?'
    cursor.execute(select_query, (id,))
    comment = cursor.fetchall()
    return comment



def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from comment")
    results = cursor.fetchone()[0]
    return (results)

def getCommentsByIdeaID(id):  # Get an idea comments with votes for each comment and information about the employee who submitted the comment
    select_query = 'SELECT *,(SELECT COUNT(*) FROM commentVote where comment.id=commentVote.commentId and commentVote.type=1) as upVotes, (SELECT COUNT(*) FROM commentVote where comment.id=commentVote.commentId and commentVote.type=0) as downVotes '\
                    'FROM idea INNER JOIN  comment  ' \
                    'ON idea.id = comment.ideaId  ' \
                    'INNER JOIN employee  ' \
                    'ON employee.id = comment.employeeId  ' \
                    'WHERE idea.id=? ' \
                    'ORDER BY comment.time DESC'
    cursor.execute(select_query, (id,))
    commentsWithVotes = cursor.fetchall()
    return commentsWithVotes

