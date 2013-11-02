__author__ = 'saasbook'
import tornado.ioloop
import tornado.web
import os
import json
import logging
from control import ShutterSpeedController
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


# send the index file
class IndexHandler(tornado.web.RequestHandler):
    def get(self, url='/'):
        logging.info("Get %s" % url)
        self.render('index.html')

    def post(self, url='/'):
        logging.info("Post %s" % url)
        self.render('index.html')


# handle commands sent from the web browser
class CommandHandler(tornado.web.RequestHandler):
    #both GET and POST requests have the same responses
    def get(self, url='/'):
        logging.info("Get %s" % url)
        self.handle_request()

    def post(self, url='/'):
        logging.info("Post %s" % url)
        self.handle_request()

    # handle both GET and POST requests with the same function
    def handle_request(self):
        # is op to decide what kind of command is being sent
        op = self.get_argument('op', None)
        logging.info("Requested operation is %s", op)
        #received a "checkup" operation command from the browser:
        if op == "checkup":
            #make a dictionary
            status = {"server": True, "mostRecentSerial": ""}
            #turn it to JSON and send it to the browser
            result = json.dumps(status)
            logging.info("Responding to <%s> with <%s>", op, result)
            self.write(result)

        #operation was not one of the ones that we know how to handle
        else:
            print(op)
            print(self.request)
            raise tornado.web.HTTPError(404, "Missing argument 'op' or not recognized")


def main():
    tornado.options.parse_command_line()
    cwd = os.getcwd()  # used by static file server
    print("Current working dir : %s" % cwd)
    # adds event handlers for commands and file requests
    application = tornado.web.Application([
        #all commands are sent to http://*:port/com
        #each command is differentiated by the "op" (operation) JSON parameter
        (r"/(com.*)", CommandHandler),
        (r"/", IndexHandler),
        (r"/(index\.html)", tornado.web.StaticFileHandler, {"path": cwd}),
        (r"/(.*\.png)", tornado.web.StaticFileHandler, {"path": cwd}),
        (r"/(.*\.jpg)", tornado.web.StaticFileHandler, {"path": cwd}),
        (r"/(.*\.js)", tornado.web.StaticFileHandler, {"path": cwd}),
        (r"/(.*\.css)", tornado.web.StaticFileHandler, {"path": cwd}),
    ])
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    main()
