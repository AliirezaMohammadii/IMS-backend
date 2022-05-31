import json
import re
import sys
from datetime import datetime

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

def get_table_size(cursor):
    cursor.execute("select * from idea")
    results = cursor.fetchall()
    return len(results)


def getIdeaByID(id):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT *  FROM idea INNER JOIN employee ON idea.employeeId = employee.id WHERE idea.id=?'
    cursor.execute(select_query, (id,))
    idea = cursor.fetchone()
    close_db()

    try:
        if idea is None:
            return NOT_FOUND

        idea_row_dict = dict(idea)
        return json.dumps(idea_row_dict)

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def create(data):
    employeeId = json.loads(employee_DB.get_by_personal_id(personal_id=data["personal_id"]))["id"]
    db = get_db()
    cursor = db.cursor()

    id              = get_table_size(cursor) + 1
    categoryId      = data["categoryId"]
    title           = data["title"]
    text            = data["text"]
    costReduction   = 0.0
    time            = datetime.now()
    status          = "NotChecked"

    insert_query = 'INSERT INTO idea (id, employeeId, categoryId, title, text, costReduction, time, status) ' \
                   'VALUES (?,?,?,?,?,?,?,?)'
    fields = (id, employeeId, categoryId, title, text, costReduction, time, status)

    try:
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
    
    employeeId      = data["employeeId"]
    categoryId      = data["categoryId"]
    title           = data["title"]
    text            = data["text"]
    costReduction   = data["costReduction"]
    time            = data["time"]
    status          = data["status"]
    
    update_query = 'UPDATE idea SET employeeId=?,categoryId=?, title=?,text=?,costReduction=?,time=?, status=?' \
                   'WHERE id=?'
    fields = (employeeId,categoryId, title,text,costReduction,time, status , id)

    try:
        if getIdeaByID(id) == NOT_FOUND:
            return NOT_FOUND

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

    query = 'DELETE FROM idea WHERE id=?'
    fields = (id,)

    try:

        if getIdeaByID(id) == NOT_FOUND:
            return NOT_FOUND

        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR

# get an employee's ideas + corresponding up/down votes + employee info
def getIdeaByEmployeePersonalId(personal_id):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes , (SELECT COUNT(*) FROM comment where idea.id=comment.ideaId) as commentsCount'\
                    'FROM idea INNER JOIN employee  ' \
                    'ON idea.employeeId = employee.id ' \
                    'WHERE employee.personal_id=?' \
                    'ORDER BY idea.time DESC'


    try:
        cursor.execute(select_query, (personal_id,))
        ideas = cursor.fetchall()
        close_db()
        return convert_to_json(ideas)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


# TODO
# pagination_id must be handled ??

#get all ideas with their votes
def getIdeas(pagination_id):
    db = get_db()
    cursor = db.cursor()
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT * , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes , (SELECT COUNT(*) FROM comment where idea.id=comment.ideaId) as commentsCount'\
                    'FROM idea INNER JOIN employee  ' \
                    'ON idea.employeeId = employee.id ' \
                    'ORDER BY idea.time DESC'
    try:
        cursor.execute(select_query)
        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR

#get an idea with its votes by ideaID
def getIdeaVotes(id):
    db = get_db()
    cursor = db.cursor()
    
    select_query = 'SELECT idea.* , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes , (SELECT COUNT(*) FROM comment where idea.id=comment.ideaId) as commentsCount'\
        'FROM idea'\
            'WHERE idea.id=?'

    try:
        cursor.execute(select_query, (id,))
        ideaWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideaWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def getIdeasByIdeaCategoryID(id):
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT * , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes , (SELECT COUNT(*) FROM comment where idea.id=comment.ideaId) as commentsCount'\
                    'FROM idea INNER JOIN employee  ' \
                    'ON idea.employeeId = employee.id  INNER JOIN ideaCategory ON ideaCategory.id = idea.categoryId' \
                    'WHERE idea.categoryId =?'\
                    'ORDER BY idea.time DESC'
                    


    try:
        cursor.execute(select_query, (id,))
        ideasWithVotesByCategory = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotesByCategory)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


# TODO
def idea_is_for_user(employeeId, idea_id):
    select_query = 'SELECT employeeId '\
                    'FROM idea ' \
                    'WHERE idea.id =?'
                    


    try:
        cursor.execute(select_query, (idea_id,))
        data = dict(cursor.fetchone())
        employeeID = data['employeeId']
        close_db()

        return (employeeId == employeeID)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR

    return False

# TODO
def like_idea(id):
    return MESSAGE_OK

# TODO
def dislike_idea(id):
    return MESSAGE_OK


def get_all_ideas():
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT * , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes , (SELECT COUNT(*) FROM comment where idea.id=comment.ideaId) as commentsCount'\
                    'FROM idea INNER JOIN employee  ' \
                    'ON idea.employeeId = employee.id ' \
                    'ORDER BY idea.time DESC'

    try:
        cursor.execute(select_query)
        ideas = cursor.fetchall()
        close_db()
        return convert_to_json(ideas)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def clear_table():
    db = get_db()
    cursor = db.cursor()
    query = 'DELETE FROM idea'
    cursor.execute(query)
    db.commit()
    close_db()

    return 'Idea table Has been cleared succesfully.'


