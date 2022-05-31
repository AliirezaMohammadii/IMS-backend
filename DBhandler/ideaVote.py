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


def create(data):
    db = get_db()
    cursor = db.cursor()

    id = get_table_size(cursor) +1
    employeeId = data["employeeId"]
    ideatId = data["commentId"]
    type = data["type"]
    time = datetime.datetime.now()

    insert_query = 'INSERT INTO ideaVote (id,employeeId, ideaId,type,time) ' \
                   'VALUES (?,?, ?,?,?)'
    fields = (id,employeeId, ideaId ,type,time)
    try:
        if  getIdeaVoteByEmployeeIdea(employeeID , ideaID) is not None:
            return IDEAVOTE_ALREADY_EXISTS
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
    type = data["type"]
    time = data["time"]

    update_query = 'UPDATE ideaVote SET employeeId=?, ideaId=?,type=?,time=?' \
                   'WHERE id=?'
    fields = (employeeId, ideaId,type,time , id)
    try:
        res = getIdeaVoteByEmployeeIdea(employeeId, ideaId)
        if res in None:
            return NOT_FOUND
        if type ==res['type'] : # double upvotes ==> No vote  # double downvotes ==> No vote 
            delete(ideaId ,  employeeId )
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

    query = 'DELETE ideaVote WHERE id=?'
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

def delete(personal_id , ideaId):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE ideaVote '\
            'WHERE  ideaVote.ideaId IN'\
            '(SELECT idea.id from idea WHERE idea.id=?)'\
            'AND ideaVote.employeeId IN'\
            '(SELECT emplyee.id from employee WHERE employee.personal_id=?)'
            
    fields = (ideaId,personal_id, )
    if getIdeaVoteByEmployeeIdea(employeeId, ideaId) is None:
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



def getIdeaVoteByEmployeeIdea(employeeID , ideaID):
    select_query = 'SELECT * ideaVote INNER JOIN idea '\
            'ON  ideaVote.ideaId= idea.id INNER JOIN employee '\
            'ON ideaVote.employeeId = employee.id'\
            'WHERE ideaVote.employeeId=? AND ideaVote.ideaId=?'
            
    fields = (employeeID,ideaID, )
    cursor.execute(select_query, fields)
    ideaVote = cursor.fetchone()
    return ideaVote

def get_table_size():
    cursor.execute("select * from ideaVote")
    results = cursor.fetchall()
    return len(results)





def clear_table():
    db = get_db()
    cursor = db.cursor()
    query = 'DELETE FROM ideaVote'
    cursor.execute(query)
    db.commit()
    close_db()

    return 'ideaVote table Has been cleared succesfully.'
