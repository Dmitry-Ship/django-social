from utils import responses
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions


def custom_404(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Http404 as err:
            return responses.failed_response(err.__str__(), status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist as err:
            return responses.failed_response(err.__str__(), status.HTTP_404_NOT_FOUND)
    return wrap


def custom_permission_denied(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except exceptions.PermissionDenied as err:
            return responses.failed_response(err.__str__(), status.HTTP_403_FORBIDDEN)
    return wrap
