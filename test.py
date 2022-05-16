import json, sys

# windows
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend')

from DBhandler import db
from DBhandler import employee as employee_DB

data_dict = {
    'firstName' : 'Ali',
    'lastName' : 'Mo',
    'username' : '1234',
    'password' : '1111',
    'mobile' : '09121111111',
    'email' : 'a@b.com',
    'committeeMember' : True,
}

data_json = json.dumps(data_dict)

error = employee_DB.create(data_json)

print('error:', error)
print('--------------------')

data = employee_DB.get_by_personal_id('1234')

print(data)

