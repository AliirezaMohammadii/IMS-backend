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
from ideaStatus import *
from DBhandler import employee as employee_DB
from DBhandler import ideaVote as ideaVote_DB

def create(data):
    db = get_db()
    cursor = db.cursor()
    employeeId = json.loads(employee_DB.get_by_personal_id(data['personal_id']))["id"]
    db = get_db()
    cursor = db.cursor()
    id = get_table_size(cursor) +1
    ideaId = data["ideaId"]
    text = data["text"]
    time = datetime.now()

    insert_query = 'INSERT INTO comment (id,employeeId, ideaId,text,time) ' \
                   'VALUES (?,?, ?,?,?)'
    fields = (id,employeeId, ideaId,text,time)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR



def update(data,id):
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
        if getCommentByID(id) == NOT_FOUND:
            return NOT_FOUND
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

    query = 'DELETE FROM comment WHERE id=?'
    fields = (id,)

    try:
        if getCommentByID(id) == NOT_FOUND:
            return NOT_FOUND

        cursor.execute(query, fields)
        db.commit()
        close_db()

        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


            
def getCommentByID(id):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * FROM comment WHERE id=?'
    cursor.execute(select_query, (id,))
    comment = cursor.fetchall()
    try:
        if commet is None:
            return NOT_FOUND
        comment_row_dict = dict(comment)
        return json.dumps(comment_row_dict)

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from comment")
    results = cursor.fetchone()[0]
    if results is None :
        return 0
    return (results)

def getCommentsByIdeaID(id):  # Get an idea comments with votes for each comment and information about the employee who submitted the comment

    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT  idea.id , comment.id , comment.employeeId , comment.text, comment.time , employee.personal_id , employee.firstName , employee.lastName ,ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  '\
                    'FROM idea INNER JOIN comment ON idea.id = comment.ideaId INNER JOIN employee ON comment.employeeId=employee.id '\
                    'LEFT JOIN ( SELECT commentVote.commentId , commentVote.type ,count(commentVote.type) as cntUP FROM commentVote Where commentVote.type is not null and commentVote.type =1 Group BY (commentVote.commentId) ) C ON C.commentId = comment.id '\
                    'LEFT JOIN ( SELECT commentVote.commentId , commentVote.type ,count(commentVote.type) as cntDOWN FROM commentVote Where commentVote.type is not null and commentVote.type =2 Group BY (commentVote.commentId) ) D ON D.commentId = comment.id '\
                    'Where idea.id=? Order BY comment.time DESC'\


                    

    cursor.execute(select_query, (id,))
    commentsWithVotes = cursor.fetchall()
    return commentsWithVotes



def getCommentsByIdeaID(id):  # Get an idea comments with votes for each comment and information about the employee who submitted the comment

    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT  comment.id , comment.employeeId , comment.text, comment.time , employee.personal_id , employee.firstName , employee.lastName ,ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  '\
                    'FROM comment INNER JOIN employee ON comment.employeeId=employee.id '\
                    'LEFT JOIN ( SELECT commentVote.commentId , commentVote.type ,count(commentVote.type) as cntUP FROM commentVote Where commentVote.type is not null and commentVote.type =1 Group BY (commentVote.commentId) ) C ON C.commentId = comment.id '\
                    'LEFT JOIN ( SELECT commentVote.commentId , commentVote.type ,count(commentVote.type) as cntDOWN FROM commentVote Where commentVote.type is not null and commentVote.type =2 Group BY (commentVote.commentId) ) D ON D.commentId = comment.id '\
                    'Where comment.ideaId=? Order BY comment.time DESC'\

                    

    try:
        cursor.execute(select_query, (id,))
        comments = cursor.fetchall()
        close_db()
        return convert_to_json(comments)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR
