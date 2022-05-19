
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity
import json
from flask_jwt_extended import get_jwt_identity


### ERROR MESSAGES
MESSAGE_OK = 0
DB_ERROR = -1

NOT_FOUND = 1
WRONG_PASSWORD = 2
USER_ALREADY_EXISTS = 3


### STATUS CODES
STATUS_OK           = 200
STATUS_CREATED      = 201

STATUS_BAD_REQUEST  = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN    = 403
STATUS_NOT_FOUND    = 404


def log(to_print):
    print('#LOG -> ', end='')
    print(to_print)


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