import time, datetime

class RequestTimingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # ---------------------------------------------------------
        # Code to be executed for each request BEFORE
        # the view (and later middleware) are called.
        # ---------------------------------------------------------
        start_time = time.time()

        # Call the next middleware or the view
        response = self.get_response(request)

        # ---------------------------------------------------------
        # Code to be executed for each request/response AFTER
        # the view is called.
        # ---------------------------------------------------------
        duration = time.time() - start_time
        print(f"{datetime.datetime.now()} - User: {request.user} - Path: {request.path}")


        return response