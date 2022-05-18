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
    categoryId = data["categoryId"]
    title = data["title"]
    text = data["text"]
    costReduction = data["costReduction"]
    time = datetime.datetime.now()
    status = ideaStatus.NotChecked
    insert_query = 'INSERT INTO idea (id,employeeId,categoryId, title,text,costReduction,time, status) ' \
                   'VALUES (?,?,?,?,?,?,?,?)'
    fields = (id,employeeId,categoryId, title,text,costReduction,time, status)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "idea insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - idea insert Failed"
        return None



def update(json,id):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)
   
    employeeId = data["employeeId"]
    categoryId = data["categoryId"]
    title = data["title"]
    text = data["text"]
    costReduction = data["costReduction"]
    time = data["time"]
    status = ideaStatus.NotChecked
    
    update_query = 'UPDATE idea SET employeeId=?,categoryId=?, title=?,text=?,costReduction=?,time=?, status=?' \
                   'WHERE id=?'
    fields = (employeeId,categoryId, title,text,costReduction,time, status , id)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "idea insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - idea insert Failed"
        return None

def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE idea WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "idea deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete idea"
        return None

def getIdeaByID(id):
    select_query = 'SELECT * FROM idea WHERE id=?'
    cursor.execute(select_query, (id,))
    idea = cursor.fetchall()
    return idea



def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from idea")
    results = cursor.fetchall()
    close_db()
    return len(results)


def getIdeaByEmployeeUsername(personal_id):
    select_query = 'SELECT * FROM idea INNER JOIN BY employee  ' \
                    'ON idea.employeeId = employee.id ' \
                    'WHERE employee.personal_id=?' \
                    'ORDER BY idea.time DESC'
    cursor.execute(select_query, (personal_id,))
    ideas = cursor.fetchall()
    return ideas



   

def getIdeas():
    select_query = 'SELECT idea.* , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes'\
        'FROM idea'\
        'ORDER BY idea.time DESC'
    cursor.execute(select_query)
    ideasWithVotes = cursor.fetchall()
    return ideasWithVotes

def getIdeaVotes(id):
    select_query = 'SELECT idea.* , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes'\
        'FROM idea'\
            'WHERE idea.id=?'
    cursor.execute(select_query, (id,))
    ideaWithVotes = cursor.fetchall()
    return ideaWithVotes

def getIdeasByIdeaCategoryID(id):
    select_query = 'SELECT idea.* , (SELECT COUNT(*) FROM ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=1) as upVotes , (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes'\
        'FROM idea WHERE idea.categoryId =?'\
        'ORDER BY idea.time DESC'
    cursor.execute(select_query, (id,))
    ideasWithVotesByCategory = cursor.fetchall()
    return ideasWithVotesByCategory


# to do : search by title