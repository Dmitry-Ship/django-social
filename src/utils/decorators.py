from utils.errors import MissingParameter


def require_parameter(parameter):
    def wrap(method):
        def wrapped_f(*args, **kwargs):
            query = args[0].request.query_params.get(parameter, None)

            if query is None:
                raise MissingParameter(parameter=parameter)

            return method(*args, **kwargs, query=query)
        return wrapped_f
    return wrap

