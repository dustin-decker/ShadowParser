import threading
import subprocess
import parsers.nginxParser
from time import sleep
import server.socketClient


# import server.socketServer

# server.socketServer.start()


def followLog(filename, type):
    threading.Thread(target=tailHandler, args=(filename, type)).start()


def tailHandler(filename, type):
    p = subprocess.Popen(["tail", "-f", filename], stdout=subprocess.PIPE)
    while 1:
        sleep(0.1)
        line = str(p.stdout.readline())
        pushToParser(line, type)
        if not line:
            break


def pushToParser(line, type):
    if type == 'nginx':
        event = parsers.nginxParser.parse(line)
        pushToServer(event)
    else:
        pass


def pushToServer(event):
    print(event)
    # server.socketClient.push(event)


followLog('/var/log/nginx/access.log', 'nginx')
