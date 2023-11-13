import socket
from status_code import StatusCode, GameMessage
import pickle

# Client configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    game_msg_dta = client_socket.recv(256)
    
    game_msg = pickle.loads(game_msg_dta) 
    
    """
    data = pickle.dumps(StatusCode.IN_TURN)
                
    client_socket.send(data)
                
    data = client_socket.recv(1024)
                
    reconstructed_data = pickle.loads(data)    
    """
    if game_msg.status_code == StatusCode.IN_TURN:
        # Get card color and type from the user
        card_color = input("Enter card color (Red, Green, Blue, Yellow): ")
        card_type = input("Enter card type (0-9, Skip, Reverse, Draw2): ")
    
        # Send the card data to the server
        card_data = f"{card_color} {card_type}"
        client_socket.send(card_data.encode('utf-8'))
    elif game_msg.status_code == StatusCode.NOTIFICATION:
        print(game_msg.data)

client_socket.close()
