
import khayyam
from datetime import timedelta
from khayyam import *
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
def getAwardBYEmployeeIdIdeaId(employeeId , ideaId, cursor) : 
    select_query = 'SELECT * FROM award WHERE award.employeeId=? and award.ideaId=?  '
    cursor.execute(select_query, (employeeId , ideaId,))
    employeeAward = cursor.fetchone()
    print(employeeAward)
    return employeeAward

def create(employeeId,ideaId,type,value):
    db = get_db()
    cursor = db.cursor()

    id = get_table_size(cursor) +1
    time = solar_date_now()

    insert_query = 'INSERT INTO award (id, employeeId, ideaId , type ,value, time) ' \
                   'VALUES (?,?,?,?,?,?)'
    fields = (id, employeeId,ideaId , type ,value, time)
    try:
        res = getAwardBYEmployeeIdIdeaId(employeeId , ideaId, cursor)
        if res is not None:
            print(res)
            print("exists")
            return AWARD_ALREADY_EXISTS
        # insert into db:
        cursor.execute(insert_query, fields)
        db.commit()
        close_db()
        print("done")
        return MESSAGE_OK

    except sqlite3.Error:  
        print("oo")
        close_db()
        return DB_ERROR



def update(data):
    db = get_db()
    cursor = db.cursor()
        
    employeeId = data["employeeId"]
    ideaId = data["ideaId"]
    type = data["type"]
    value = data["value"]
    time = data["time"]
    update_query = 'UPDATE award SET employeeId =?,ideaId =?,type =?,value =?, time =?' \
                   'WHERE id=?'
    fields = ( employeeId,ideaId , type ,value, time, id)
    try:
        if getAwardByID(id) == NOT_FOUND:
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

    query = 'DELETE FROM award WHERE id=?'
    fields = (id,)

    try:

        if getAwardByID(id) is None:
            return NOT_FOUND

        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR

def deleteALL():
    db = get_db()
    cursor = db.cursor()

    query = 'DELETE FROM award '

    try:

        cursor.execute(query)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR

def getAwardByUsername(personal_id):  # Awards received by an employee.
    select_query = 'SELECT * FROM award INNER JOIN employee ON employee.id = award.employeeId WHERE employee.personal_id=? '
    cursor.execute(select_query, (personal_id,))
    employeeAward = cursor.fetchall()
    return employeeAward

def getAwards():    # All awards given so far.
    select_query = 'SELECT * FROM award INNER JOIN employee ON employee.id = award.employeeId'
    cursor.execute(select_query)
    awards = cursor.fetchall()
    return awards


def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from award")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)

def test_date():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()
    firstDayOfLastMonth = JalaliDate(source_date.year, source_date.month-1, 1)
    lastDayOfLastMonth = JalaliDate(source_date.year, source_date.month-1, 31)
    firstDayOfLastYear = JalaliDate(source_date.year-1, 1, 1)
    lastDayOfLastYear = JalaliDate(source_date.year-1, 12, 29)
    firstDayOfLastWeek=   JalaliDate(source_date -timedelta(7+JalaliDate(source_date).weekday()))
    lastDayOfLastWeek = JalaliDate(source_date -timedelta(1+JalaliDate(source_date).weekday()))


    print(JalaliDate(source_date))
    #query = "SELECT date(=?) as LastDateoftheMonth"
    #cursor.execute(query,(now,))
    #res = cursor.fetchone()[0]
    print(firstDayOfLastMonth,lastDayOfLastMonth)
    print(JalaliDatetime().now())


    #if(JalaliDate(firstDayOfLastMonth).weekday()==0):  # is shanbe :)

    #print((str(khayyam.JalaliDatetime.now())[:-10][0:4]))
    dd ={
        "now": str(khayyam.JalaliDatetime.now())[:-10],
       # "now2": JalaliDate(str(khayyam.JalaliDatetime.now())[:-10][0:4],JalaliDate(str(khayyam.JalaliDatetime.now())[:-10][4:6]),JalaliDate(str(khayyam.JalaliDatetime.now())[:-10][6:8])),
        "firstDayOfLastMonth":firstDayOfLastMonth,
        "lastDayOfLastMonth":lastDayOfLastMonth,
        "firstDayOfLastYear":firstDayOfLastYear,
        "lastDayOfLastYear":lastDayOfLastYear,
        "firstDayOfLastWeek":firstDayOfLastWeek,
        "lastDayOfLastWeek":lastDayOfLastWeek,
        "ruz":JalaliDate(firstDayOfLastMonth).weekday(),
        "solarSTR":str(khayyam.JalaliDatetime.now())[:-10],
        "solarDATE":JalaliDatetime(str(khayyam.JalaliDatetime.now())[:-10]),
    }
    return dd




def getAwardByID(id, cursor) : 
    select_query = 'SELECT * FROM award WHERE id=?   '
    cursor.execute(select_query, (id,))
    employeeAward = cursor.fetchall()
    print("_________________")
    print(dict(employeeAward))
    print("_________________")
    return employeeAward


def sumAwardsValue():
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT SUM(award.value) as awardvalues  '\
                    'FROM award  '


    try:
        cursor.execute(select_query)
        value = cursor.fetchone()
        close_db()
        return json.dumps(dict(value))

    except sqlite3.Error:  
        close_db()
        return DB_ERROR