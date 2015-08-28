import tornado.ioloop
import tornado.web
import tornado.websocket

clients = []


class WebSocketChatHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        clients.append(self)

    def on_message(self, message):
        print(message)
        for client in clients:
            client.write_message(message)

    def on_close(self):
        clients.remove(self)


if __name__ == '__main__':
    app = tornado.web.Application([(r'/', WebSocketChatHandler)])

    app.listen(7777)
    tornado.ioloop.IOLoop.instance().start()
