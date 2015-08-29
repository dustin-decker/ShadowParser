from websocket._core import create_connection


def push(event):
    ws = create_connection("ws://localhost:7777")
    ws.send(event.encode())
    result = ws.recv()
    print("Broadcasted :'%s'" % result)
    ws.close()


if __name__ == '__main__':
    passs
