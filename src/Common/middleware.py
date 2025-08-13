


class CorsAllowAllOrigin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'content-type,x-csrftoken'

        return response


class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #for header, value in request.headers.items():
        #    print(f'{header}: {value}')
        print(f'Origin: {request.headers.get("origin")}')
        print('***')
        print()
        response = self.get_response(request)

        return response
