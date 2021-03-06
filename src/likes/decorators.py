from utils import responses
from rest_framework import status
from .errors import AlreadyLiked


def handle_likes_errors(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except AlreadyLiked as err:
            return responses.failed_response(err.__str__(), status.HTTP_400_BAD_REQUEST)
    return wrap
