class Error(Exception):
    pass


class parameterMissing(Error):
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f'parameter {self.parameter} is missing'