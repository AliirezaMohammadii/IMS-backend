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
    cursor.execute("select max(ifnull(id,0)) from tpi")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)


def create(data):
    db = get_db()
    cursor = db.cursor()

    id = get_table_size(cursor) + 1
    jwt_token = data["jwt_token"]
    personal_id = data["personal_id"]

    print('\ncreate - jwt_token:', jwt_token)
    print('create - personal_id:', personal_id)

    insert_query = 'INSERT INTO tpi (id, jwt_token, personal_id) ' \
                   'VALUES (?, ?, ?)'
    fields = (id, jwt_token, personal_id)

    try:
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        print('create - Ok')
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def get(jwt_token):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT personal_id FROM tpi WHERE jwt_token=?'
    cursor.execute(select_query, (jwt_token,))
    personal_id = dict(cursor.fetchone())['personal_id']

    close_db()

    return personal_id
