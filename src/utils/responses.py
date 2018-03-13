from rest_framework.response import Response


def failed_response(error=None, status=None, headers=None):
    response = {'status': False}
    if error:
        response = {**response, 'error': error}
    return Response(response, status=status, headers=headers)


def successful_response(data=None, status=None, headers=None):
    response = {'status': True}
    if data:
        response = {**response, 'data': data}
    return Response(response, status=status, headers=headers)
