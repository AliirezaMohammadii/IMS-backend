import json
import re
import sys

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


def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from evaluationCriteria")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)

def checkIfExists(title , cursor) : 
    select_query = 'SELECT * FROM evaluationCriteria WHERE evaluationCriteria.title=?   '
    cursor.execute(select_query, (title,))
    crit = cursor.fetchone()
    print(crit)
    return crit


def create(data):
    db = get_db()
    cursor = db.cursor()

    id = get_table_size(cursor)+1
    title = data["title"]
    weight = data["weight"]
    insert_query = 'INSERT INTO evaluationCriteria (id, title, weight) ' \
                   'VALUES (?,?, ?)'
    fields = (id, title, weight)
    		

    try:	
        res = checkIfExists(title, cursor)
        if res is not None:
            return EVCRITS_ALREADY_EXISTS
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
    
    title = data["title"]
    weight = data["weight"]
    update_query = 'UPDATE evaluationCriteria SET title =?, weight =?' \
                   'WHERE id=?'
    fields = (title, weight , id)
    try:
        if getEvaluationCriteriaByID(id, cursor) is None:
            return NOT_FOUND
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def get_all_ev_crits():
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * FROM evaluationCriteria'

    try:
        cursor.execute(select_query)
        ev_crits = cursor.fetchall()
        close_db()
        return convert_to_json(ev_crits)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def delete_by_id(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM evaluationCriteria WHERE id=?'
    fields = (id,)

    try:
        if getEvaluationCriteriaByID(id, cursor) is None:
            return NOT_FOUND

        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR

def delete_by_title(title):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM evaluationCriteria WHERE title=?'
    fields = (title,)

    try:
        if checkIfExists(title, cursor) is None:
            return NOT_FOUND

        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR
        
def clear_table():
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM evaluationCriteria '
    try:
        cursor.execute(query)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR

# def getEvaluationCriteriaByID(id):
#     select_query = 'SELECT * FROM evaluationCriteria WHERE id=?'
#     cursor.execute(select_query, (id,))
#     evaluationCriteria = cursor.fetchall()
#     return evaluationCriteria

def getEvaluationCriteriaByID(id,cursor):
    select_query = 'SELECT * FROM evaluationCriteria WHERE id=?'
    cursor.execute(select_query, (id,))
    crits = cursor.fetchall()
    return convert_to_json(crits)