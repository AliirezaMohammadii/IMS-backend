import json
import re
import sys
import datetime

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


def create(data):
    db = get_db()
    cursor = db.cursor()

    id          = get_table_size(cursor) + 1
    employeeId  = employee_DB.get_user_id(data["personal_id"])
    commentId   = data["commentId"]
    type        = data["type"]
    time        = solar_date_now()

    insert_query = 'INSERT INTO commentVote (id,employeeId, commentId,type,time) ' \
                   'VALUES (?,?,?,?,?)'
    fields = (id, employeeId, commentId, type, time,)

    try:
        if getCommentVoteByEmployeeComment(employeeId , commentId, cursor) is not None:
            return COMMENTVOTE_ALREADY_EXISTS

        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def update(data, id): 
    db = get_db()
    cursor = db.cursor()

    employeeId = employee_DB.get_user_id(data["personal_id"])
    commentId = data["commentId"]
    type = data["type"]
    time = data["time"]

    update_query = 'UPDATE commentVote SET employeeId=?, commentId=?,type=?,time=? ' \
                   'WHERE id=?'
    fields = (employeeId, commentId,type,time , id)
    try:
        res = getCommentVoteByEmployeeComment(employeeId, commentId)
        if res in None :
            return NOT_FOUND
        if   type ==res['type'] : # double upvotes ==> No vote  # double downvotes ==> No vote 
            delete(commentId , employeeId)
            return MESSAGE_OK
            
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

    query = 'DELETE FROM commentVote WHERE id=?'
    fields = (id,)
    if getCommentVoteByID(id) is None:
            return NOT_FOUND
    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def delete(commentId, employeeId):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM commentVote '\
            'WHERE  commentVote.commentId = ? and '\
            'commentVote.emplyee.id = ?  '
            
    fields = (commentId,employeeId, )
    if getCommentVoteByEmployeeComment(employeeId , commentId, cursor) is None:
        return NOT_FOUND
    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def getCommentVoteByID(id):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * FROM commentVote WHERE id=?'
    cursor.execute(select_query, (id,))
    commentVote = cursor.fetchall()

    close_db()
    return commentVote


def getCommentVoteByEmployeeComment(employeeID , commentID,cursor):
    select_query = 'SELECT * FROM commentVote '\
            'WHERE commentVote.employeeId=? AND commentVote.commentId=? '
            
    fields = (employeeID,commentID, )
    cursor.execute(select_query, fields)
    commentVote = cursor.fetchone()
    return commentVote


def getCommentVoteByEmployeePersonalIDCommentID(personalID, commentID):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * commentVote INNER JOIN comment '\
            'ON  commentVote.commentId= comment.id INNER JOIN employee '\
            'ON commentVote.employeeId = employee.id'\
            'WHERE employee.personal_id=? AND commentVote.commentId=?'
            
    fields = (personalID,commentID, )
    cursor.execute(select_query, fields)
    commentVote = cursor.fetchone()
    return commentVote
    

def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from commentVote")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)


def like_comment(commentId, employeeId):
    data_dict = {
        'employeeId': employeeId,
        'commentId': commentId,
        'type': 1,
    }
    message = create(data_dict)
    if message == COMMENTVOTE_ALREADY_EXISTS:
        message = update(data_dict)

    return message


def dislike_comment(commentId, employeeId):
    data_dict = {
        'employeeId': employeeId,
        'commentId': commentId,
        'type': 2,
    }
    message = create(data_dict)
    if message == COMMENTVOTE_ALREADY_EXISTS:
        message = update(data_dict)

    return message


def clear_table():
    db = get_db()
    cursor = db.cursor()
    query = 'DELETE FROM commentVote'
    cursor.execute(query)
    db.commit()
    close_db()

    return 'CommentVote table Has been cleared succesfully.'
    