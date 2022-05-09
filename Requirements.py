
STATUS_OK           = 200
STATUS_CREATED      = 201

STATUS_BAD_REQUEST  = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN    = 403
STATUS_NOT_FOUND    = 404


def user_is_logged_in(session):
    if 'username' in  session:
        return True

    return False