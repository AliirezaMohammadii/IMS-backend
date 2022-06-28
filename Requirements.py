
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import get_jwt_identity, create_access_token, get_jwt, get_jwt_identity
import json
from hashlib import sha256
# from khayyam import JalaliDateTime as JDateTime
import khayyam
import sys

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

### STATUS CODES
STATUS_OK           = 200
STATUS_CREATED      = 201

STATUS_BAD_REQUEST  = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN    = 403
STATUS_NOT_FOUND    = 404

STATUS_INTERNAL_SERVER_ERROR = 500


ADMIN_personal_id = '11111111'


# Token to PersonalId
tpi = {}


def is_admin(personal_id):
    return personal_id == ADMIN_personal_id


def get_personal_id(request):
    jwt_token = request.headers['Authorization'].split()[1]
    personal_id = tpi[jwt_token]
    return personal_id


def log(to_print):
    print('#LOG -> ', end='')
    print(to_print)


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
    if diff > 0:
        diff_str = str(diff) + ' ساعت قبل'

    else:
        minute = int(time.split()[-1][-2:])
        diff = int(solar_date_now()[-2:]) - minute
        diff = 60 + diff if diff < 0 else diff

        if diff == 0:
            diff_str == 'چند لحظه قبل'
        else:
            diff_str = str(diff) + ' دقیقه قبل'

    return diff_str


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
