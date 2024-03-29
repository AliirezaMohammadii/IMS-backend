
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import get_jwt_identity, create_access_token, get_jwt, get_jwt_identity
import json
from hashlib import sha256
#from khayyam import JalaliDateTime as JDateTime
import khayyam
import sys
from sansorchi import Sansorchi


# windows
sys.path.insert(0, 'C://Users//asus//Desktop//Uni//SW Eng//Project//project files//venv//IMS//backend')
# macOs
sys.path.insert(0, '/Users/mohammad/Documents/Github/IMS-backend')


### ERROR MESSAGES
MESSAGE_OK = 0
DB_ERROR = -1

NOT_FOUND = 1
WRONG_PASSWORD = 2
USER_ALREADY_EXISTS = 3
IDEAVOTE_ALREADY_EXISTS = 4
CATEGORY_ALREADY_EXISTS = 5
COMMENTVOTE_ALREADY_EXISTS = 6
SCORE_HEADER_ALREADY_EXISTS = 7
SCORE_DETAIL_ALREADY_EXISTS = 8
AWARD_ALREADY_EXISTS = 9
EVCRITS_ALREADY_EXISTS = 10
CAT_ALREADY_EXISTS  = 11
RUDE_CONCEPT = 12

### STATUS CODES
STATUS_OK           = 200
STATUS_CREATED      = 201

STATUS_BAD_REQUEST  = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN    = 403
STATUS_NOT_FOUND    = 404

STATUS_INTERNAL_SERVER_ERROR = 500


def log(to_print):
    print('#LOG -> ', end='')
    print(to_print)


def has_rude_concept(text):
    sansorchi = Sansorchi()
    return sansorchi.is_bad_word(text)


def remove_bad_words(text):
    sansorchi = Sansorchi()
    return sansorchi.remove_bad_words(text, replace_text='***')


def solar_date_now():
    return str(khayyam.JalaliDatetime.now())[:-10]


def hash_password(password):
    # hash_password = sha256(password.encode('utf-8')).hexdigest()
    # return hash_password
    return password


def convert_to_json(data):
    data = list(map(lambda x:dict(x), data))
    return json.dumps(data, separators=(',', ':'))


def fix_time_diff(time):
    diff_str = ''

    hour = int(time.split()[-1][-5:-3])
    diff = int(solar_date_now()[-5:-3]) - hour

    if diff < 0:
        minute = int(time.split()[-1][-2:])
        diff = int(solar_date_now()[-2:]) - minute
        diff = 60 + diff if diff < 0 else diff

        if diff == 0:
            diff_str = 'چند لحظه قبل'
        else:
            diff_str = str(diff) + ' دقیقه قبل'

        return diff_str

    else:
        return time


def convert_to_json_editTime(data):
    data = list(map(lambda x:dict(x), data))

    for i in range(len(data)):
        time = str(data[i]['time'])
        data[i]['time'] = fix_time_diff(time)

    return json.dumps(data, separators=(',', ':'))


def update_jwt_if_expired(response):
    
    exp_timestamp = get_jwt()['exp']
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(minutes=15))

    if target_timestamp > exp_timestamp:
        data = response.get_json()
        if type(data) is dict:
            # update access_token
            access_token = create_access_token(identity=get_jwt_identity())
            data['access_token'] = access_token     # Then in front side, this must be checked and updated.
            response.data = json.dumps(data)

    return response



def revoke_jwt():
    # create some random access token, and frontend side is not supposed to be informed.
    create_access_token(identity=get_jwt_identity())


def check_is_logged_in():
    return get_jwt_identity()
