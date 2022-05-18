import json
import re
import sys
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
    type = data["type"]
    value = data["value"]
    time = datetime.datetime.now()

    insert_query = 'INSERT INTO award (id, employeeId,ideaId , type ,value, time) ' \
                   'VALUES (?,?,?,?,?,?)'
    fields = (id, employeeId,ideaId , type ,value, time)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "award insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - award insert Failed"
        return None



def update(json,id):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)
    
    employeeId = data["employeeId"]
    ideaId = data["ideaId"]
    type = data["type"]
    value = data["value"]
    time = data["time"]
    update_query = 'UPDATE award SET employeeId =?,ideaId =?,type =?,value =?, time =?' \
                   'WHERE id=?'
    fields = ( employeeId,ideaId , type ,value, time, id)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "award updated successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - award update Failed"
        return None

def delete(id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE award WHERE id=?'
    fields = (id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "award deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete award"
        return None



def getAwardByUsername(personal_id):  # Awards received by an employee.
    select_query = 'SELECT * FROM award INNER JOIN BY employee ON employee.id = award.employeeId WHERE employee.personal_id=?'
    cursor.execute(select_query, (personal_id,))
    employeeAward = cursor.fetchall()
    return employeeAward

def getAwards():    # All awards given so far.
    select_query = 'SELECT * FROM award INNER JOIN BY employee ON employee.id = award.employeeId'
    cursor.execute(select_query)
    awards = cursor.fetchall()
    return awards

def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from award")
    results = cursor.fetchall()
    close_db()
    return len(results)