from rest_framework.response import Response
from rest_framework.views import exception_handler


def failed_response(error=None, status=None, headers=None):
    return Response({'error': error}, status=status, headers=headers)


def successful_response(data=None, status=None, headers=None):
    return Response({'data': data}, status=status, headers=headers)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data = dict({'error': response.data})

    return response


def successful(method):
    def wrap(*args, **kwargs):
        response = method(*args, **kwargs)
        my_data = dict({'data': response.data})
        response.data = my_data
        return response
    return wrap


def successful_response_decorator(cls):
    class Wrapper(cls):
        def __init__(self, *args):
            super(Wrapper, self).__init__(*args)

        def __getattribute__(self, name):
            view_methods = ['retrieve', 'update', 'create', 'destroy']

            method = cls.__getattribute__(self, name)
            if method is None:
                view_methods.append('list')

            if name in view_methods:
                return successful(method)
            else:
                return method

    return Wrapper
