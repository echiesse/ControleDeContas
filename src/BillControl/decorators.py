
def cors_allow_origin(origin):
    def decorator(cls):
        _dispatch = cls.dispatch

        def wrapper(method):
            def action(self, request, *args, **kwargs):
                response = method(self, request, *args, **kwargs)
                response.headers['Access-Control-Allow-Origin'] = origin
                return response
            return action

        cls.dispatch = wrapper(_dispatch)
        return cls

    return decorator
