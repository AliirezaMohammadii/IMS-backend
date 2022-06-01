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
    cursor.execute("select max(ifnull(id,0)) from ideaCategory")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)


def create(data):
    db = get_db()
    cursor = db.cursor()

    id = get_table_size(cursor) + 1
    title = data["title"]

    insert_query = 'INSERT INTO ideaCategory (id, title) ' \
                   'VALUES (?,?)'
    fields = (id, title)

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
    
    title = data["title"]

    update_query = 'UPDATE ideaCategory SET title =?' \
                   'WHERE id=?'
    fields = (title , id)

    try:
        if getIdeaCategoryByID(id , cursor ) is NONE:
            return NOT_FOUND
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def get_all_categories():
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT * FROM ideaCategory'

    try:
        cursor.execute(select_query)
        idea_categories = cursor.fetchall()
        close_db()
        return convert_to_json(idea_categories)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def getIdeaCategoryByID(id,cursor):
    select_query = 'SELECT * FROM ideaCategory WHERE id=?'
    cursor.execute(select_query, (id,))
    ideaCategory = cursor.fetchall()
    return ideaCategory

def getIdeaCategoryByTitle(title, cursor):
    select_query = 'SELECT * FROM ideaCategory WHERE title=?'
    cursor.execute(select_query, (title,))
    ideaCategory = cursor.fetchall()
    return ideaCategory

def clear_table():
    db = get_db()
    cursor = db.cursor()
    query = 'DELETE FROM ideaCategory'
    cursor.execute(query)
    db.commit()
    close_db()

    return 'ideaCategory table Has been cleared succesfully.'

