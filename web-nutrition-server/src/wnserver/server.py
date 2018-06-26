#!/usr/bin/env python
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from wnserver.analyzer import Analyzer


# HTTPRequestHandler class
class RestServer(BaseHTTPRequestHandler):
    
    analyzer = Analyzer()
    
    # GET
    def do_GET(self):
        request = urlparse(self.path)
        
        if request.path == '/nutrition':
            #validate HTTP param exists
            if not request.query:
                self.respond(400, {'error': 'The following GET parameters are required: "url"'})
            else:
                query_def=parse_qs(request.query)
                
                #validate HTTP params
                if not 'url' in query_def:
                    self.respond(400, {'error': 'Missing GET parameter "url"'})
                else:
                    url = query_def['url'][0]
                    #respond to valid request
                    result = self.analyzer.analyze(url)
                    if 'error' in result:
                        self.respond(200, {
                            'url': url,
                            'status': 'error',
                            'error': result['error']
                        })
                    else:
                        self.respond(200, {
                            'url': url,
                            'status': 'ok',
                            'nutrition': result
                        })
        else:
            self.respond(400, {'error': 'Unknown request URL. Do GET to /nutrition for web nutrition analysis'})
        return
 
    # response is a python dict, will be converted into JSON
    def respond(self, status_code, response):
        # HTTP Status Code (200 = OK, 400 = Bad Request)
        self.send_response(status_code)
        
        # HTTP Header
        self.send_header('Content-type','text/json')
        # allow this REST API to be accessed no matter on which website our chrome extension runs:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Convert response into JSON and send
        self.wfile.write(bytes(json.dumps(response), "utf8"))


def run(port):
    print('starting wnserver...')
    
    # Server settings
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, RestServer)
    print('running wnserver...')
    httpd.serve_forever()


if __name__ == "__main__":
    run(8080)
