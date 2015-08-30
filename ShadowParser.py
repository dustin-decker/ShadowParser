import threading
import subprocess
import parsers.nginxParser
from time import sleep
import tornado.ioloop
import tornado.web
import tornado.websocket


class ShadowParser(tornado.websocket.WebSocketHandler):

    def open(self, *args):
        self.followlog('/var/log/nginx/access.log', 'nginx')
        print("WebSocket opened")

    def on_message(self, message):
        print(message)
        self.write_message(message)

    def on_close(self):
        print("WebSocket closed")

    # allow for cross-origin request
    def check_origin(self, origin):
        return True

    def followlog(self, filename, logtype):
        threading.Thread(target=self.tailhandler,
                         name=filename,
                         args=(filename, logtype)).start()

    def tailhandler(self, filename, logtype):
        p = subprocess.Popen(["tail", "-f", filename], stdout=subprocess.PIPE)
        while 1:
            sleep(0.1)
            line = str(p.stdout.readline())
            self.parseandserve(line, logtype)
            if not line:
                break

    def parseandserve(self, line, logtype):
        event = 0
        if logtype == 'nginx':
            event = parsers.nginxParser.parse(line)
        else:
            pass

        if event:
            self.write_message(event)
        else:
            pass


if __name__ == '__main__':
    app = tornado.web.Application([(r'/', ShadowParser)])
    app.listen(7777)
    tornado.ioloop.IOLoop.instance().start()
