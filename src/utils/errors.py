from rest_framework.exceptions import APIException


class MissingParameter(APIException):
    status_code = 401

    def __init__(self, parameter):
        self.parameter = parameter

    @property
    def detail(self):
        return f'Parameter {self.parameter} is missing'
