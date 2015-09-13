from threading import Thread
import pika
from pygtail import Pygtail
import json
from time import sleep


class ShadowFollower:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='loglines')
        self.followlog('/var/log/nginx/access.log', 'nginx')
        while True:
            pass

    def followlog(self, filename, logtype):
        Thread(target=self.tailhandler,
               name=filename,
               args=(filename, logtype),
               daemon=True).start()

    def tailhandler(self, filename, logtype):
        while True:
            for line in Pygtail(filename, offset_file=logtype):
                self.push(line, logtype)
                print(line)
                sleep(0.1)

    def push(self, event, logtype):
        if self.channel:
            jsonbody = json.dumps(event, logtype).encode()
            self.channel.basic_publish(exchange='',
                                       routing_key='loglines',
                                       body=jsonbody)
            print('Broadcasted: ' % event.encode())


if __name__ == '__main__':
    app = ShadowFollower()
