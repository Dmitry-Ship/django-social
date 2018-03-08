from rest_framework.response import Response


def failed_response(error=None):
    response = {'status': False}
    if error:
        response = {**response, 'error': error}
    return Response(response)


def successful_response(data=None):
    response = {'status': True}
    if data:
        response = {**response, 'data': data}
    return Response(response)
