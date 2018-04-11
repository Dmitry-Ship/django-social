from utils import responses
from rest_framework import status
from .errors import SelfFollowing, NotFollowing


def handle_follow_errors(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except SelfFollowing as err:
            return responses.failed_response(err.__str__(), status.HTTP_400_BAD_REQUEST)
        except NotFollowing as err:
            return responses.failed_response(err.__str__(), status.HTTP_404_NOT_FOUND)
    return wrap