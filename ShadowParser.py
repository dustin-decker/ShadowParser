import parsers.nginxParser
import tornado.ioloop
import tornado.web
import tornado.websocket
import queue

eventqueue = queue.Queue()


class ShadowParser(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print('WebSocket opened')
        self.followqueue()

    def on_message(self, message):
        print(message)
        self.write_message(message)

    def on_close(self):
        print('WebSocket closed')

    # allow for cross-origin request
    def check_origin(self, origin):
        return True

    def followqueue(self):
        while True:
            line, logtype = eventqueue.get()
            self.parseandserve(line, logtype)
            eventqueue.task_done()

    def parseandserve(self, line, logtype):
        event = 0
        if logtype == 'nginx':
            event = parsers.nginxParser.parse(line)
        if event:
            self.write_message(event)


class EventQueueHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print('WebSocket opened')

    def on_message(self, message):
        print('eventqueue.put: ' + message)
        eventqueue.put(message)
        self.write_message(message)

    def on_close(self):
        print('WebSocket closed')

    # allow for cross-origin request
    def check_origin(self, origin):
        return True


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', ShadowParser),
        (r'/events', EventQueueHandler)
    ])
    app.listen(7777)
    tornado.ioloop.IOLoop.instance().start()
