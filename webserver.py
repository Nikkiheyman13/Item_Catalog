from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Beer, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB ##
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/beer"):
                beers = session.query(Beer).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                for beer in beers:
                    output += beer.name
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def main():
        try:
            port = 5000
            server = HTTPServer(('', port), WebServerHandler)
            print "Web Server running on port %s" % port
            server.serve_forever()
        except KeyboardInterrupt:
            print " ^C entered, stopping web server...."
            server.socket.close()

if __name__ == '__main__':
        main()
