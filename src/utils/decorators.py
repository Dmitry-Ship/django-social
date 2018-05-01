from utils import responses
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions
from utils.errors import parameterMissing


def handle_404(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Http404 as err:
            return responses.failed_response(err.__str__(), status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist as err:
            return responses.failed_response(err.__str__(), status.HTTP_404_NOT_FOUND)
    return wrap


def handle_permission_denied(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except exceptions.PermissionDenied as err:
            return responses.failed_response(err.__str__(), status.HTTP_403_FORBIDDEN)
    return wrap


def handle_parameter_missing(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except parameterMissing as err:
            return responses.failed_response(err.__str__(), status.HTTP_400_BAD_REQUEST)
    return wrap


def require_parameter(parameter):
    def wrap(method):
        def wrapped_f(*args, **kwargs):
            query = args[0].request.query_params.get(parameter, None)

            if query is None:
                raise parameterMissing(parameter)

            return method(*args, **kwargs, query=query)
        return wrapped_f
    return wrap

