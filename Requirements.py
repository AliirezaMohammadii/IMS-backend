
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity
import json


STATUS_OK           = 200
STATUS_CREATED      = 201

STATUS_BAD_REQUEST  = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN    = 403
STATUS_NOT_FOUND    = 404


def log(to_print):
    print('#LOG -> ', end='')
    print(to_print)


def user_is_logged_in(session):
    if 'personal_id' in session:
        # print(session['personal_id'])
        return True

    # print('session is empty')
    return False


def update_jwt_if_expired(response):
    
    exp_timestamp = get_jwt()['exp']
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(minutes=15))

    if target_timestamp > exp_timestamp:
        access_token = create_access_token(identity=get_jwt_identity())
        data = response.get_json()

        if type(data) is dict:  # if we have valid response with 'access_token' key
            data['access_token'] = access_token
            response.data = json.dumps(data)

    return response