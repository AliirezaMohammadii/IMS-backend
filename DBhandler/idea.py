
import json
import re
import sys
from datetime import datetime
import random
import khayyam
from datetime import timedelta
from khayyam import *
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
from DBhandler import employee as employee_DB
from DBhandler import ideaVote as ideaVote_DB
from DBhandler import award as award_DB
from DBhandler import ideaStatus


def get_table_size(cursor):
    cursor.execute("select max(ifnull(id,0)) from idea")
    results = cursor.fetchone()[0]
    if results is None:
        return 0
    return (results)


def getIdeaByID(id):
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id WHERE idea.id=? Order BY idea.time DESC'\

    
    cursor.execute(select_query, (id,))
    idea = cursor.fetchone()
    close_db()

    try:
        if idea is None:
            return NOT_FOUND

        idea_row_dict = dict(idea)
        return json.dumps(idea_row_dict)

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def getIdeaByID_loggedIn(id, personal_id):
    
    db = get_db()
    cursor = db.cursor()

    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(userVote,0) vote , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type as userVote from ideaVote inner join employee on employee.id = ideaVote.employeeId Where employee.personal_id =? ) S ON S.ideaId = idea.id LEFT JOIN totalScore ON totalScore.ideaId =idea.id  WHERE idea.id=? Order BY idea.time DESC'

    
    cursor.execute(select_query, (personal_id,id , ))
    idea = cursor.fetchone()
    close_db()

    try:
        if idea is None:
            return NOT_FOUND

        idea_row_dict = dict(idea)
        return json.dumps(idea_row_dict)

    except sqlite3.Error:
        close_db()
        return DB_ERROR


def create(data):
    db = get_db()
    cursor = db.cursor()

    id              = get_table_size(cursor) + 1
    employeeId      = employee_DB.get_user_id(data["personal_id"])
    categoryId      = data["categoryId"]
    title           = data["title"]
    text            = data["text"]
    costReduction   = 0.0
    time            = solar_date_now()
    status          = 'NotChecked'
    
    insert_query = 'INSERT INTO idea (id, employeeId, categoryId, title, text, costReduction, time, status) ' \
                   'VALUES (?,?,?,?,?,?,?,?)'
    fields = (id, employeeId, categoryId, title, text, costReduction, time, status)

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
    
    employeeId      = employee_DB.get_user_id(data["personal_id"])
    categoryId      = data["categoryId"]
    title           = data["title"]
    text            = data["text"]
    costReduction   = data["costReduction"]
    time            = data["time"]
    status          = data["status"]
    
    update_query = 'UPDATE idea SET employeeId=?,categoryId=?, title=?,text=?,costReduction=?,time=?, status=?' \
                   'WHERE id=?'
    fields = (employeeId,categoryId, title,text,costReduction,time, status , id)

    try:
        if getIdeaByID(id) == NOT_FOUND:
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

    query = 'DELETE FROM idea WHERE id=?'
    fields = (id,)

    try:
        if getIdeaByID(id) is None:
            return NOT_FOUND

        cursor.execute(query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:
        close_db()
        return DB_ERROR


# get an employee's ideas + corresponding up/down votes + employee info
def getIdeaByEmployeePersonalId(personal_id):
    db = get_db()
    cursor = db.cursor()

    #select_query = 'SELECT Count(*) FROM idea INNER JOIN ideaVote ON idea.id=ideaVote.ideaId Where ideaVote.type is NOT NULL and ideaVote.type=1 '
    #, (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes , (SELECT COUNT(*) FROM comment where idea.id=comment.ideaId) as commentsCount
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount  , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        ' WHERE employee.personal_id=? Order BY idea.time DESC'\

    try:
        cursor.execute(select_query,(personal_id,))
        ideas = cursor.fetchall()
        close_db()
        return convert_to_json(ideas)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


# TODO
# pagination_id must be handled ??

#get all ideas with their votes
def getIdeas(pagination_id):
    db = get_db()
    cursor = db.cursor()
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                            'WHERE idea.status != ? '\
                        'Order BY idea.status ASC , idea.time DESC'\

    try:
        cursor.execute(select_query,('NotChecked',))
        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR

def getBestIdeasByUsersALL():
    db = get_db()
    cursor = db.cursor()
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? '\
                        'Order BY  upvotes - downvotes  DESC , idea.time DESC '\
                        'LIMIT 10'

    try:
        cursor.execute(select_query,('NotChecked',))
        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR




def getBestIdeasByUsersMONTH():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()
    firstDayOfLastMonth = str(JalaliDatetime(source_date.year, source_date.month-1, 1))[0:-10]
    lastDayOfLastMonth  = str(JalaliDatetime(source_date.year, source_date.month-1, 31,23,59))[0:-10]
    #print(firstDayOfLastMonth)
    #print(lastDayOfLastMonth)
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and idea.time >= ? and idea.time <= ? '\
                        'Order BY  upvotes - downvotes  DESC , idea.time DESC '\
                        'LIMIT 10'
    #select_query = 'SELECT idea.time FROM idea '
    try:
        cursor.execute(select_query,('NotChecked',firstDayOfLastMonth,lastDayOfLastMonth,))
        #cursor.execute(select_query)

        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def getBestIdeasByUsersWEEK():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()

    firstDayOfLastWeek=   str(JalaliDate(source_date -timedelta(7+JalaliDate(source_date).weekday())))
    lastDayOfLastWeek = str(JalaliDate(source_date -timedelta(1+JalaliDate(source_date).weekday())))

    #print(firstDayOfLastWeek)
    #print(lastDayOfLastWeek)
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and substr(idea.time,0,11) >= ? and substr(idea.time,0,11) <= ? '\
                        'Order BY  upvotes - downvotes  DESC , idea.time DESC '\
                        'LIMIT 10'
    #select_query = 'SELECT substr(idea.time,0,11) FROM idea '
    try:
        cursor.execute(select_query,('NotChecked',firstDayOfLastWeek,lastDayOfLastWeek,))
        #cursor.execute(select_query)

        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR





def getBestIdeasByCommitteeALL():
    db = get_db()
    cursor = db.cursor()
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and idea.status != ? '\
                        'Order BY  meanScore  DESC , idea.time DESC '\
                        'LIMIT 10'

    try:
        cursor.execute(select_query,('NotChecked','Rejected'))
        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR




def getBestIdeasByCommitteeMONTH():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()
    firstDayOfLastMonth = str(JalaliDatetime(source_date.year, source_date.month-1, 1))[0:-10]
    lastDayOfLastMonth  = str(JalaliDatetime(source_date.year, source_date.month-1, 31,23,59))[0:-10]
    #print(firstDayOfLastMonth)
    #print(lastDayOfLastMonth)
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and idea.status != ? and idea.time >= ? and idea.time <= ? '\
                        'Order BY  meanScore  DESC , idea.time DESC '\
                        'LIMIT 10'

    #select_query = 'SELECT idea.time FROM idea '
    try:
        cursor.execute(select_query,('NotChecked','Rejected',firstDayOfLastMonth,lastDayOfLastMonth,))
        #cursor.execute(select_query)

        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def getBestIdeasByCommitteeWEEK():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()

    firstDayOfLastWeek=   str(JalaliDate(source_date -timedelta(7+JalaliDate(source_date).weekday())))
    lastDayOfLastWeek = str(JalaliDate(source_date -timedelta(1+JalaliDate(source_date).weekday())))

    #print(firstDayOfLastWeek)
    #print(lastDayOfLastWeek)
    # ideas + upvotes + down_votes + employees info
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and idea.status != ? and substr(idea.time,0,11) >= ? and substr(idea.time,0,11) <= ? '\
                        'Order BY  meanScore  DESC , idea.time DESC '\
                        'LIMIT 10'
    #select_query = 'SELECT substr(idea.time,0,11) FROM idea '
    try:
        cursor.execute(select_query,('NotChecked','Rejected',firstDayOfLastWeek,lastDayOfLastWeek,))
        #cursor.execute(select_query)

        ideasWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR




def awardBestIdeasByCommitteeWEEK():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()
    firstDayOfLastWeek=   str(JalaliDate(source_date -timedelta(7+JalaliDate(source_date).weekday())))
    lastDayOfLastWeek = str(JalaliDate(source_date -timedelta(1+JalaliDate(source_date).weekday())))
    select_query = 'SELECT  idea.employeeId, idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and idea.status != ? and substr(idea.time,0,11) >= ? and substr(idea.time,0,11) <= ? '\
                        'Order BY  meanScore  DESC , idea.time DESC '\
                        'LIMIT 10'
    try:
        cursor.execute(select_query,('NotChecked','Rejected',firstDayOfLastWeek,lastDayOfLastWeek,))
        ideas = cursor.fetchall()
        close_db()
        
        for idea in ideas:
            
            res = award_DB.create(dict(idea)['employeeId'], dict(idea)['id'], 'committee', 2000000)
        return res

    except sqlite3.Error:  
        close_db()
        return DB_ERROR








def awardBestIdeasByCommitteeMONTH():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()
    firstDayOfLastMonth = str(JalaliDatetime(source_date.year, source_date.month-1, 1))[0:-10]
    lastDayOfLastMonth  = str(JalaliDatetime(source_date.year, source_date.month-1, 31,23,59))[0:-10]
    select_query = 'SELECT  idea.employeeId ,idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and idea.status != ? and idea.time >= ? and idea.time <= ? '\
                        'Order BY  meanScore  DESC , idea.time DESC '\
                        'LIMIT 10'
    try:
        cursor.execute(select_query,('NotChecked','Rejected',firstDayOfLastMonth,lastDayOfLastMonth,))
        ideas = cursor.fetchall()
        close_db()
        print(ideas)
        for idea in ideas:
            print("idea = = = " , dict(idea))
            res = award_DB.create(dict(idea)['employeeId'], dict(idea)['id'], 'committee', 2000000)
        return res

    except sqlite3.Error:  
        close_db()
        return DB_ERROR







def awardBestIdeasByCommitteeALL():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()

    select_query = 'SELECT  idea.employeeId ,idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status != ? and idea.status != ? '\
                        'Order BY  meanScore  DESC , idea.time DESC '\
                        'LIMIT 10'
    try:
        cursor.execute(select_query,('NotChecked','Rejected',))
        ideas = cursor.fetchall()
        close_db()
        print(ideas)
        for idea in ideas:
            print("idea = = = " , dict(idea))
            res = award_DB.create(dict(idea)['employeeId'], dict(idea)['id'], 'committee', 2000000)
        return res

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


















def awardBestIdeasByLotteryMONTH():
    db = get_db()
    cursor = db.cursor()
    source_date = khayyam.JalaliDatetime.now()
    firstDayOfLastMonth = str(JalaliDatetime(source_date.year, source_date.month-1, 1))[0:-10]
    lastDayOfLastMonth  = str(JalaliDatetime(source_date.year, source_date.month-1, 31,23,59))[0:-10]
    select_query = 'SELECT  idea.employeeId ,idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount , ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  '\
                        'WHERE idea.status = ?  and idea.time >= ? and idea.time <= ? '\
                        'Order BY  meanScore  DESC , idea.time DESC '\
                        'LIMIT 10'
    try:
        cursor.execute(select_query,('Rejected',firstDayOfLastMonth,lastDayOfLastMonth,))
        ideas = cursor.fetchall()
        close_db()
        print(ideas)
        rowOfWinner  = random.randint(0, len(ideas))
        idea = ideas[rowOfWinner]
        print("idea = = = " , dict(idea))
        res = award_DB.create(dict(idea)['employeeId'], dict(idea)['id'], 'committee', 2000000)
        return res

    except sqlite3.Error:  
        close_db()
        return DB_ERROR




def costReductionValue():
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT SUM(idea.costReduction)  '\
                    'FROM idea  '\
                        'WHERE idea.status=? '\

    try:
        cursor.execute(select_query, ('Implemented',))
        value = cursor.fetchone()[0]
        close_db()
        return convert_to_json(value)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR

def ideasCount():
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT Count(*)  '\
                    'FROM idea  '

    try:
        cursor.execute(select_query)
        value = cursor.fetchone()[0]
        close_db()
        return convert_to_json(value)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR



def thinkersList():
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT Distinct employee.* FROM idea INNER JOIN employee ON idea.employeeId=employee.id  '\

    try:
        cursor.execute(select_query)
        value = cursor.fetchall()
        close_db()
        return convert_to_json(value)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR










#get an idea with its votes by ideaID
def getIdeaVotes(id):
    db = get_db()
    cursor = db.cursor()
    
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount ,ifnull(totalScore.meanScore,0) meanScore  '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id WHERE idea.id=? '\
                        'Order BY idea.time DESC'\

    try:
        cursor.execute(select_query, (id,))
        ideaWithVotes = cursor.fetchall()
        close_db()
        return convert_to_json(ideaWithVotes)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def getIdeasByIdeaCategoryID(id):
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount ,ifnull(totalScore.meanScore,0) meanScore  '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id  INNER JOIN ideaCategory ON ideaCategory.id = idea.categoryId'\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  '\
                        'LEFT JOIN totalScore ON totalScore.ideaId =idea.id  WHERE idea.categoryId=? '\
                        'Order BY idea.time DESC'\

    try:
        cursor.execute(select_query, (id,))
        ideasWithVotesByCategory = cursor.fetchall()
        close_db()
        return convert_to_json(ideasWithVotesByCategory)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR













def idea_is_for_user(employeeId, idea_id):
    db = get_db()
    cursor = db.cursor()
    select_query = 'SELECT employeeId '\
                    'FROM idea ' \
                    'WHERE idea.id =?'

    try:
        cursor.execute(select_query, (idea_id,))
        data = dict(cursor.fetchone())
        employee_ID = data['employeeId']
        close_db()

        if (int(employeeId) - int(employee_ID)) == 0:
            return True
        else:
            return False

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def like_idea(ideaId, employeeId):
    data_dict = {
        'employeeId': employeeId,
        'ideaId': ideaId,
        'type': 1,
    }

    message = ideaVote_DB.create(data_dict)
    if message == IDEAVOTE_ALREADY_EXISTS:
        message = ideaVote_DB.update(data_dict)

    return message


def dislike_idea(ideaId, employeeId):
    data_dict = {
        'employeeId': employeeId,
        'ideaId': ideaId,
        'type': 2,
    }

    message = ideaVote_DB.create(data_dict)
    if message == IDEAVOTE_ALREADY_EXISTS:
        message = ideaVote_DB.update(data_dict)

    return message


def get_all_ideas():
    db = get_db()
    cursor = db.cursor()

    #select_query = 'SELECT Count(*) FROM idea INNER JOIN ideaVote ON idea.id=ideaVote.ideaId Where ideaVote.type is NOT NULL and ideaVote.type=1 '
    #, (SELECT COUNT(*) FROM  ideaVote where idea.id=ideaVote.ideaId and ideaVote.type=0) as downVotes , (SELECT COUNT(*) FROM comment where idea.id=comment.ideaId) as commentsCount
    select_query = 'SELECT  idea.id , idea.categoryId , idea.title ,idea.text , idea.costReduction , idea.time , idea.status , employee.personal_id , employee.firstName , employee.lastName , ifnull(cntUP,0) upvotes  ,  ifnull(cntDOWN,0) downvotes  , ifnull(cntComments,0) commentsCount ,ifnull(totalScore.meanScore,0) meanScore '\
                    'FROM idea INNER JOIN employee ON idea.employeeId =employee.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntUP FROM ideaVote Where ideaVote.type is not null and ideaVote.type =1 Group BY (ideaVote.ideaId) ) C ON C.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT ideaVote.ideaId , ideaVote.type ,count(ideaVote.type) as cntDOWN FROM ideaVote Where ideaVote.type is not null and ideaVote.type =2 Group BY (ideaVote.ideaId) ) D ON D.ideaId = idea.id '\
                    'LEFT JOIN ( SELECT comment.ideaId ,count(comment.id) as cntComments FROM comment ) E ON E.ideaId = idea.id  LEFT JOIN totalScore ON totalScore.ideaId =idea.id Order BY idea.time DESC'\

    try:
        cursor.execute(select_query)
        ideas = cursor.fetchall()
        close_db()
        return convert_to_json(ideas)

    except sqlite3.Error:  
        close_db()
        return DB_ERROR


def clear_table():
    db = get_db()
    cursor = db.cursor()
    query = 'DELETE FROM idea'
    cursor.execute(query)
    db.commit()
    close_db()

    return 'Idea table Has been cleared succesfully.'


def change_idea_status(idea_id, data):

    db = get_db()
    cursor = db.cursor() 

    status = data['status']

    update_query = 'UPDATE idea SET status = ? WHERE id = ?'
    fields = (status, idea_id)
                   
    try:
        if getIdeaByID(idea_id) == NOT_FOUND:
            return NOT_FOUND

        cursor.execute(update_query, fields)
        db.commit()
        close_db()
        return MESSAGE_OK

    except sqlite3.Error:  
        close_db()
        return DB_ERROR

