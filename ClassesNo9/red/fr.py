import kua.routes as k 
from kua import RouteError
from wsgiref.simple_server import make_server
import chevron
from urllib.parse import parse_qs

def out_html(data, template, start_response, status='200 OK', headers = None):
    if headers is None:
        headers = []
    with open(template, 'r') as f:
        response_body = chevron.render(f, data).encode()
    headers = headers + [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body)))
    ]
    start_response(status, headers)
    return [response_body]
    
def redir303(url, start_response, headers = None):
    if headers is None:
        headers = []
    headers = headers + [('Location', url)]
    start_response('303 See Other', headers)
    return []

def form_data(environ, keys):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    return {k:d.get(k.encode(), [b''])[0].decode() for k in keys}

class Server:
    def __init__(self):
        self._routes = k.Routes()

    def route(self, path):
        def inner(f):
            self._routes.add(path, f)
            print(f'Added path {path}')
            return f 
        return inner 
    
    def _app(self, environ, start_response):
        path = environ['PATH_INFO']
        try:
            route = self._routes.match(path)
        except RouteError:
            return out_html({'path':path}, '404.html', start_response, status='404 Not Found')
        else:
            environ['route.params']  = route.params
            return route.anything(environ, start_response)

    def run(self, host="", port=8080):
        with make_server(host, port, self._app) as httpd:
            print(f"Serving on port {port}...")
            httpd.serve_forever()