#!/usr/bin/env python3
#
# WHO
#
#  km@grogg.org
#
# WHAT
#
#  Simple HTTP server that will dump out all JSON POST requests sent
#
# -----------------------------------------------------------------------------
# imports {{{
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.request import Request
from urllib.request import urlopen
import json
import logging
import argparse
import ssl


# }}}
# class JSONDumper(SimpleHTTPRequestHandler): {{{
# -----------------------------------------------------------------------------
class JSONDumper(SimpleHTTPRequestHandler):

    def _send_response(self, code):
        """Send a nice response"""

        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        return


# }}}
# -----------------------------------------------------------------------------

    def do_GET(self):
        """Handle GET requests"""

        logging.info("GET request,\nPath: %s\nHeaders:\n%s", str(self.path),
                     str(self.headers))

        self._send_response(200)
        self.wfile.write("GET request for {}".format(
            self.path).encode('utf-8'))

        return


# }}}
# -----------------------------------------------------------------------------

    def do_POST(self):
        """Handle POST requests"""

        # Get the data size & read the data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Extract JSON
        try:
            json_data = json.loads(post_data)
            post_data = json.dumps(json_data, indent=4, sort_keys=False)
        except:
            json_data = None
#            post_data = "ERROR: No JSON data found"

        logging.info(">>> POST\nPATH: %s\nHEADERS:\n%sBODY:\n%s\n",
                     str(self.path), str(self.headers), post_data)

        # Always be content - Philippians 4:11
        self._send_response(200)
        logging.info("POST request for %s", self.path.encode('utf-8'))

        return


# }}}
# def main(port): {{{
# -----------------------------------------------------------------------------
def main(port, ssl):

    logging.basicConfig(level=logging.INFO)

    httpd = HTTPServer(('', port), JSONDumper)
    logging.info('Started HTTPd on port %i', port)
    if ssl:
        httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='privkey.pem',
                                       certfile='server.pem', server_side=True)

    # Go on forever
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info('Stopped HTTPd')


# }}}
# if __name__ == '__main__': {{{
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description='jsondumper')
    parser.add_argument('--port', '-p', type=int, default=81,
                        help='Port to listen on. Default is 81')
    parser.add_argument('--ssl', '-s', action='store_true', help='Use SSL')
    args = parser.parse_args()

    main(args.port, args.ssl)


# }}}
