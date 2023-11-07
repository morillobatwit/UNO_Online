import socket
import threading

host = '127.0.0.1'
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(50)

clients = []
usernames = []

def sendToAll(message):
    for client in clients:
        client.send(message)

def handle_client(cs, addr):
    index = clients.index(cs)
    name = usernames[index]
    while True:
        try:
            message = cs.recv(1024)
            if message:
                sendToAll(f"{name}: {message.decode('utf-8')}".encode('utf-8'))
        except:
            cs.remove(cs)
            usernames.remove(name)
            sendToAll(f"{name} has left the chat.".encode('utf-8'))
            cs.close()
            break

def recvConnections():
    while True:
        print('Waiting for connections...')
        cs, addr = s.accept()
        print(f"Connection established with {addr}")

        name = cs.recv(1024).decode('utf-8')
        usernames.append(name)
        clients.append(cs)
        
        print(f"The username of the connected user is {name}")
        sendToAll(f"{name} has joined".encode('utf-8'))
        
        thread = threading.Thread(target=handle_client, args=(cs, addr))
        thread.start()

recvConnections()

