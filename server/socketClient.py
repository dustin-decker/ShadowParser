from socket import create_connection

def push(event):
    ws = create_connection("ws://localhost:8666/websocket")
    print(event)
    ws.send(event)
    ws.close()