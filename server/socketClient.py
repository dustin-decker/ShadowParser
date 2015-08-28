from socket import create_connection

def push(event):
    ws = create_connection(('localhost', 7777))
    print(event)
    ws.send(event)
    ws.close()


if __name__ == '__main__':
    pass