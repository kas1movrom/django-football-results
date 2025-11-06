import logging
import time


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers["ABRAKADABRA"] = "sniff"
        return response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        logging.info(f"REQUEST METHOD: {request.method}")
        logging.info(f"URL: {request.headers.get('Referer')}{request.path.lstrip('/')}")
        logging.info(f"IP ADDRESS: {request.META.get('REMOTE_ADDR')}")
        start_time = time.time()
        response = self.get_response(request)
        result = time.time() - start_time
        logging.info(f"TIME: {result}")
        return response
