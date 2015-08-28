import tornado.ioloop
import tornado.web
import tornado.websocket


class SocketServer(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print("WebSocket opened")

    def on_message(self, message):
        print(message)
        self.write_message(message)

    def on_close(self):
        print("WebSocket closed")

    # allow for cross-origin request
    def check_origin(self, origin):
        return True


if __name__ == '__main__':
    app = tornado.web.Application([(r'/', SocketServer)])

    app.listen(7777)
    tornado.ioloop.IOLoop.instance().start()
