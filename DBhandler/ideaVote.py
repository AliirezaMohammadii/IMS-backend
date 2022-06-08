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


def create(data):    

    employeeId = employee_DB.get_user_id(data["personal_id"])
    db = get_db()
    cursor = db.cursor()
    id = get_table_size(cursor) +1
    ideaId = data["ideaId"]
    type = data["type"]
    time = solar_date_now()

    insert_query = 'INSERT INTO ideaVote (id,employeeId, ideaId,type,time) ' \
                   'VALUES (?,?, ?,?,?)'
    fields = (id,employeeId, ideaId ,type,time)
    try:
        if getIdeaVoteByEmployeeIdea(employeeId , ideaId, cursor) is not None:
            return IDEAVOTE_ALREADY_EXISTS
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR



def update(data): 
    db = get_db()
    cursor = db.cursor()

    employeeId = employee_DB.get_user_id(data["personal_id"])
    ideaId = data["ideaId"]
    type = data["type"]
    time = datetime.now()

    update_query = 'UPDATE ideaVote SET type=?,time=? ' \
                   'WHERE employeeId=? and ideaId=? '
    fields = (type,time ,employeeId, ideaId)
    try:
        res = (getIdeaVoteByEmployeeIdea(employeeId, ideaId,cursor))
        
        if res is None:
            return NOT_FOUND
        res = dict(res)
        if type == res['type'] : # double upvotes ==> No vote  # double downvotes ==> No vote 
            delete(ideaId ,  employeeId )
            print("here")
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

    query = 'DELETE FROM ideaVote WHERE id=?'
    fields = (id,)
    if getIdeaVoteByID(id) is None:
            return NOT_FOUND
    try:
        
        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR

def delete(ideaId,employeeId ):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM ideaVote '\
            'WHERE  ideaVote.ideaId = ? and  '\
            ' ideaVote.employeeId=?  '
            
    fields = (ideaId,employeeId, )
    if getIdeaVoteByEmployeeIdea(employeeId, ideaId , cursor) is None:
            return NOT_FOUND
    try:
        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def getIdeaVoteByID(id):
    select_query = 'SELECT * FROM ideaVote WHERE id=?'
    cursor.execute(select_query, (id,))
    ideaVote = cursor.fetchall()
    return ideaVote

def getIdeaVoteTypeByID(id):
    db = get_db()
    cursor = db.cursor()

    try:
        IdeaVoteRow = getIdeaVoteByID(personal_id, cursor)
        if IdeaVoteRow is None:
            return NOT_FOUND

        IdeaVoteRow_row_dict = dict(IdeaVoteRow)
        idea_vote_type = IdeaVoteRow_row_dict['type']
        close_db()
        return idea_vote_type

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def getIdeaVoteByEmployeeIdea(employeeID , ideaID,cursor):
    select_query = 'SELECT * FROM ideaVote '\
            'WHERE ideaVote.employeeId=? AND ideaVote.ideaId=? '
            
    fields = (employeeID,ideaID, )
    cursor.execute(select_query, fields)
    ideaVote = cursor.fetchone()

    return ideaVote

def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from ideaVote")
    results = cursor.fetchone()[0]
    if results is None:
        return 0

    return (results)


def clear_table():
    db = get_db()
    cursor = db.cursor()
    query = 'DELETE FROM ideaVote'
    cursor.execute(query)
    db.commit()
    close_db()

    return 'ideaVote table Has been cleared succesfully.'
