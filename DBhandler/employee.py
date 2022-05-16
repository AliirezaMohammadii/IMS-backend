import json
import re
import sys

# windows
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend//DBhandler')
# macOs
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend/DBhandler')
sys.path.insert(0, '/Users/narges/Documents/GitHub/IMS-backend/DBhandler')
from db import *


def getEmployeeByPersonalId(personal_id, cursor):
    select_query = 'SELECT * FROM employee WHERE personal_id=?'
    cursor.execute(select_query, (personal_id,))
    employees = cursor.fetchone()
    return employees


def getEmployeeByMobile(mobile, cursor):
    select_query = 'SELECT * FROM employee WHERE mobile=?'
    cursor.execute(select_query, (mobile,))
    employees = cursor.fetchone()
    return employees


def getEmployeeByEmail(email, cursor):
    select_query = 'SELECT * FROM employee WHERE email=?'
    cursor.execute(select_query, (email,))
    employees = cursor.fetchone()
    return employees


def get_table_size(cursor):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from employee")
    results = cursor.fetchall()
    close_db()
    return len(results)


def create(json):
    db = get_db()
    cursor = db.cursor()
    data = json.loads(json)
    
    id = get_table_size(cursor)+1
    password = data["password"]
    personal_id = data["personal_id"]
    firstName = data["firstName"]
    lastName = data["lastName"]
    mobile = data["mobile"]
    email = data["email"]
    committeeMember = data["committeeMember"]

   

    insert_query = 'INSERT INTO employee (id, firstName, lastName, personal_id, password, mobile , email , committeeMember) ' \
                   'VALUES (?, ?, ?, ?, ?, ?, ?)'
    fields = (firstName, lastName, personal_id, password, mobile , email , committeeMember)

    try:
        #check if employee already exists :
        if len(getEmployeeByPersonalId(personal_id, cursor))>0:
            response = "Employee already exists with this personal_id"
            return response
        if len(getEmployeeByEmail(email, cursor))>0:
            response = "Employee already exists with this email"
            return response
        if len(getEmployeeByMobile(mobile, cursor))>0:
            response = "Employee already exists with this mobile"
            return response

        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        response = "Employee registered successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - Employee registration Failed"
        return response


def update(json):
    db = get_db()
    cursor = db.cursor()

    data = json.loads(json)
    password = data["password"]
    personal_id = data["personal_id"]
    firstName = data["firstName"]
    lastName = data["lastName"]
    mobile = data["mobile"]
    email = data["email"]
    committeeMember = data["committeeMember"]

    update_query = 'UPDATE employee SET firstName =?, lastName =?, password =?, mobile  =? , email  =?, committeeMember =? ' \
                   'WHERE personal_id=?'
                   
    fields = (firstName, lastName, password, mobile , email , committeeMember, personal_id)

    try:
        #check if employee already exists :
        if  len(getEmployeeByPersonalId(personal_id, cursor))==0:
            response = "Employee does not exist with this personal_id"
            return response
        if len(getEmployeeByEmail(email,cursor))>0:
            response = "Employee already exists with this email"
            return response
        if len(getEmployeeByMobile(mobile,cursor))>0:
            response = "Employee already exists with this mobile"
            return response
            
        # insert into db:
        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        response = "Employee updated successfully."
        return response

    except sqlite3.Error:  
        close_db()
        response = "SQlite Error - Employee update Failed"
        return None



def delete(personal_id):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE employee WHERE personal_id=?'
    fields = (personal_id,)

    try:

        cursor.execute(query, fields)
        db.commit()
        close_db()

        response = "Employee deleted successfully"
        return response

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to delete employee"
        return None


def get_by_personal_id(personal_id):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    try:
        employeeRow = getEmployeeByPersonalId(personal_id , cursor)
        if len(employeeRow)==0:
            response = "Employee does not exist with this personal_id"
            return response
        employee_row_dict = dict(employeeRow)
        close_db()
        return json.dumps(employee_row_dict)

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to retrieve employee"
        return None
