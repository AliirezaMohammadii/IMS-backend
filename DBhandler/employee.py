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


def getEmployeeByPersonalId(personal_id, cursor):
    # print(personal_id)
    select_query = 'SELECT * FROM employee WHERE personal_id=?'
    cursor.execute(select_query, (personal_id,))
    employee = cursor.fetchone()
    return employee


# no need probably
def getEmployeeByMobile(mobile, cursor):
    select_query = 'SELECT * FROM employee WHERE mobile=?'
    cursor.execute(select_query, (mobile,))
    employee = cursor.fetchone()
    return employee


# no need probably
def getEmployeeByEmail(email, cursor):
    select_query = 'SELECT * FROM employee WHERE email=?'
    cursor.execute(select_query, (email,))
    employee = cursor.fetchone()
    return employee


def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from employee")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)


def create(data):
    db = get_db()
    cursor = db.cursor()

    id = get_table_size(cursor)+1
    hashed_password = hash_password(data["password"])
    personal_id     = data["personal_id"]
    firstName       = ""
    lastName        = ""
    mobile          = ""
    email           = ""
    committeeMember = True if data["committeeMember"] == 1 else False
    isAdmin = True if data["isAdmin"] == 1 else False
    
    insert_query = 'INSERT INTO employee (id, firstName, lastName, personal_id, password, mobile , email , committeeMember , isAdmin) ' \
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ? , ?)'
    fields = (id, firstName, lastName, personal_id, hashed_password, mobile, email, committeeMember,isAdmin)

    try:
        #check if employee already exists :
        if getEmployeeByPersonalId(personal_id, cursor) is not None:
            return USER_ALREADY_EXISTS

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

    hashed_password = data["password"]
    personal_id     = data["personal_id"]
    firstName       = data["firstName"]
    lastName        = data["lastName"]
    mobile          = data["mobile"]
    email           = data["email"]
    committeeMember = True if data["committeeMember"] == 1 else False
    update_query = 'UPDATE employee SET firstName =?, lastName =?, password =?, mobile  =? , email  =?, committeeMember =? ' \
                   'WHERE personal_id=?'
                   
    fields = (firstName, lastName, hashed_password, mobile, email, committeeMember, personal_id)

    try:
        if getEmployeeByPersonalId(personal_id, cursor) is None:
            return NOT_FOUND

        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def delete(personal_id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM employee WHERE personal_id=?'
    fields = (personal_id,)

    if getEmployeeByPersonalId(personal_id, cursor) is None:
        return NOT_FOUND

    try:
        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def get_by_personal_id(personal_id):
    db = get_db()
    cursor = db.cursor()

    try:
        employeeRow = getEmployeeByPersonalId(personal_id, cursor)
        if employeeRow is None:
            return NOT_FOUND

        employee_row_dict = dict(employeeRow)
        close_db()
        return json.dumps(employee_row_dict)

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def get_all_employees():
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT * FROM employee'

    try:
        cursor.execute(select_query)
        employees = cursor.fetchall()
        close_db()
        return convert_to_json(employees)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def user_exist(personal_id):
    db = get_db()
    cursor = db.cursor()
    return_value = False

    try:
        if getEmployeeByPersonalId(personal_id, cursor) is not None:
            return_value = True

        close_db()
        return return_value

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def check_password(personal_id, input_password):
    db = get_db()
    cursor = db.cursor()
    return_value = False

    select_query = 'SELECT password FROM employee WHERE personal_id=?'

    try:
        cursor.execute(select_query, (personal_id,))
        data = dict(cursor.fetchone())
        hashed_password = data['password']

        if hash_password(input_password) == hashed_password:
            return_value = True

        close_db()
        return return_value

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def get_user_id(personal_id):
    db = get_db()
    cursor = db.cursor()
    query = 'SELECT id FROM employee WHERE personal_id=?'

    try:
        cursor.execute(query, (personal_id,))
        data = dict(cursor.fetchone())
        id = int(data['id'])
        # close_db()
        return id
    
    except:
        close_db()
        return DB_ERROR


def set_as_committeeMember(personal_id):
    db = get_db()
    cursor = db.cursor()

    update_query = 'UPDATE employee SET committeeMember = ?'
    fields = (True,)
                   
    try:
        if getEmployeeByPersonalId(personal_id, cursor) is None:
            return NOT_FOUND

        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def set_as_ordinaryMember(personal_id):
    db = get_db()
    cursor = db.cursor()

    update_query = 'UPDATE employee SET committeeMember = ? WHERE personal_id=?'
    fields = (False, personal_id)
                   
    try:
        if getEmployeeByPersonalId(personal_id, cursor) is None:
            return NOT_FOUND

        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def clear_table():
    db = get_db()
    cursor = db.cursor()
    query = 'DELETE FROM employee'
    cursor.execute(query)
    db.commit()
    close_db()

    return 'Employee table Has been cleared succesfully.'
