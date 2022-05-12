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
    
    id = get_table_size(cursor)+1;
    password = data["password"]
    username = data["username"]
    firstName = data["firstName"]
    lastName = data["lastName"]
    mobile = data["mobile"]
    email = data["email"]
    committeeMember = data["committeeMember"]

   

    insert_query = 'INSERT INTO employee (id,firstName, lastName, username, password, mobile , email , committeeMember) ' \
                   'VALUES (?, ?, ?, ?, ?, ?, ?)'
    fields = (firstName, lastName, username, password, mobile , email , committeeMember)

    try:
        #check if employee already exists :
        if len(getEmployeeByUsername(username, cursor))>0:
            response = "Employee already exists with this username"
            return response
        if len(getEmployeeByEmail(email,cursor))>0:
            response = "Employee already exists with this email"
            return response
        if len(getEmployeeByMobile(mobile,cursor))>0:
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
        return None





def update(json):
    db = get_db()
    cursor = db.cursor()

    data = json.loads(json)
    password = data["password"]
    username = data["username"]
    firstName = data["firstName"]
    lastName = data["lastName"]
    mobile = data["mobile"]
    email = data["email"]
    committeeMember = data["committeeMember"]

    update_query = 'UPDATE employee SET firstName =?, lastName =?, password =?, mobile  =? , email  =?, committeeMember =? ' \
                   'WHERE username=?'
                   
    fields = (firstName, lastName, password, mobile , email , committeeMember, username)

    try:
        #check if employee already exists :
        if  len(getEmployeeByUsername(username, cursor))==0:
            response = "Employee does not exist with this username"
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



def delete(username):
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE employee WHERE username=?'
    fields = (username,)

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


def get_by_username(username):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()


    try:
        employeeRow=  getEmployeeByUsername(username , cursor)
        if len(employeeRow)==0:
            response = "Employee does not exist with this username"
            return response
        employee_row_dict = dict(employeeRow)
        close_db()
        return json.dumps(employee_row_dict)

    except sqlite3.Error:
        close_db()
        response = "SQlite Error - Failed to retrieve employee"
        return None


def getEmployeeByUsername(username):
    select_query = 'SELECT * FROM employee WHERE username=?'
    cursor.execute(select_query, (username,))
    employees = cursor.fetchone()
    return employees


def getEmployeeByMobile(mobile):
    select_query = 'SELECT * FROM employee WHERE mobile=?'
    cursor.execute(select_query, (mobile,))
    employees = cursor.fetchone()
    return employees


def getEmployeeByMobile(email):
    select_query = 'SELECT * FROM employee WHERE email=?'
    cursor.execute(select_query, (email,))
    employees = cursor.fetchone()
    return employees



def get_table_size():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from employee")
    results = cursor.fetchall()
    close_db()
    return len(results)