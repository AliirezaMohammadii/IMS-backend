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
    title = data["title"]
    
    insert_query = 'INSERT INTO ideaCategory (id, title) ' \
                   'VALUES (?,?)'
    fields = (id,title)
    try:
        
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "ideaCategory insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - ideaCategory insert Failed"
        return None



def update(json,id):
    db = get_db()
    cursor = db.cursor()
    
    data = json.loads(json)
    title = data["title"]
    update_query = 'UPDATE ideaCategory SET title =?' \
                   'WHERE id=?'
    fields = (title , id)
    try:
        
        # update db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "ideaCategory insert successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - ideaCategory insert Failed"
        return None



def getIdeaCategoryByID(id):
    select_query = 'SELECT * FROM ideaCategory WHERE id=?'
    cursor.execute(select_query, (id,))
    ideaCategory = cursor.fetchall()
    return ideaCategory



def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from ideaCategory")
    results = cursor.fetchall()
    close_db()
    return len(results)