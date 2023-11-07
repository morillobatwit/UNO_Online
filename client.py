import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1234))

name = input("Enter your name: ")
client.send(name.encode('utf-8'))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print('An error occurred.')
            client.close()
            break

def client_send():
    while True:
        message = f'{name}: {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
