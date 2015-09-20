from sys import exit
import tornado.ioloop
import tornado.web
import tornado.websocket
import pika
from threading import Thread
import logging
import parsers.nginxParser
import json


class SocketHandler(tornado.websocket.WebSocketHandler):
    def rabbitconnect(self):
        self.connection = pika.BlockingConnection()
        logging.info('Connected:localhost')
        self.channel = self.connection.channel()
        logging.info('Starting thread RabbitMQ')
        self.threadRMQ = Thread(target=self.threaded_rmq)
        self.threadRMQ.start()

    def open(self):
        logging.info('WebSocket opened')
        self.rabbitconnect()
        clients.append(self)

    def on_close(self):
        logging.info('WebSocket closed')
        clients.remove(self)

    # allow for cross-origin request
    def check_origin(self, origin):
        return True

    def threaded_rmq(self):
        self.channel.queue_declare(queue="loglines")
        logging.info('consumer ready, on loglines')
        self.channel.basic_consume(self.consumer_callback, queue="loglines", no_ack=True)
        self.channel.start_consuming()

    def disconnect_to_rabbitmq(self):
        self.channel.stop_consuming()
        self.connection.close()
        logging.info('Disconnected from Rabbitmq')

    def consumer_callback(self, ch, method, properties, body):
        logging.info("[x] Received via RabbitMQ: %r" % (body))
        body = json.loads(body.decode('utf-8'))
        body = self.parseandserve(body['event'], body['logtype'])
        logging.info("[x] Sent via websockets: %r" % (body))
        for itm in clients:
            if body:
                itm.write_message(body)

    def parseandserve(self, line, logtype):
        event = 0
        if logtype == 'nginx':
            event = parsers.nginxParser.parse(line)
        if event:
            return event


# Optional web server for hosting ShadowBuster
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ShadowBuster/index.html")


application = tornado.web.Application([
    (r'/', SocketHandler),
    (r"/web", MainHandler),
])


def startTornado():
    logging.info('Starting websocket server')
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()


def stopTornado():
    tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)


    # web socket clients connected.
    clients = []

    logging.info('Starting thread Tornado')

    threadTornado = Thread(target=startTornado)

    try:
        threadTornado.start()
    except KeyboardInterrupt:
        logging.info('Disconnecting from RabbitMQ..')
        disconnect_to_rabbitmq()
        stopTornado()
        exit(0)
