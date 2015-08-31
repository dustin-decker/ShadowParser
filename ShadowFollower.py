from websocket._core import create_connection
from threading import Thread
import subprocess
from time import sleep


class ShadowFollower:
    def __init__(self):
        self.ws = create_connection('ws://localhost:7777/events')  # this seems to be blocking...
        self.followlog('/var/log/nginx/access.log', 'nginx')

    def followlog(self, filename, logtype):
        Thread(target=self.tailhandler,
               name=filename,
               args=(filename, logtype),
               daemon=True).start()

    def tailhandler(self, filename, logtype):
        p = subprocess.Popen(['tail', '-f', filename], stdout=subprocess.PIPE)
        while True:
            sleep(0.01)
            line = str(p.stdout.readline())
            if line:
                self.push(line, logtype)

    def push(self, event, logtype):
        if self.ws:
            self.ws.send((event.encode(), logtype.encode()))
            result = self.ws.recv()
            print('Broadcasted: ' % result)


if __name__ == '__main__':
    ws = create_connection('ws://localhost:7777/events')
    app = ShadowFollower()
