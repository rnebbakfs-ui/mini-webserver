# route registration + matching 

# miniweb/router.py
from collections import defaultdict

class Router:
    def __init__(self):
        # mapping: (method, path) -> handler
        self.routes = {}

    def add_route(self, path, methods=("GET",)):
        methods = [m.upper() for m in methods]
        def decorator(func):
            for m in methods:
                self.routes[(m, path)] = func
            return func
        return decorator

    def match(self, method, path):
        # exact match first
        handler = self.routes.get((method.upper(), path))
        return handler
