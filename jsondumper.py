#!/usr/bin/env python3
"""

Simple HTTP server in python for logging requests

Usage:
    ./jsondumper.py [port]

"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

class jsondumper(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        Handle GET requests
        """

        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        """
        Handle POST requests
        """

        # Get the data size
        content_length = int(self.headers['Content-Length'])
        # Read the data
        post_data = self.rfile.read(content_length)
        # Make JSON pretty
        json_data = json.dumps(json.loads(post_data), indent=4, sort_keys=False)

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
               str(self.path), str(self.headers), json_data)

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=jsondumper, port=81):

    logging.basicConfig(level=logging.INFO)

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd\n')

    # Go on forever
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info('Stopping httpd\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        print('\nUsage: ./jsondumper.py <port>\n')

