import socket
import threading
import pickle
from status_code import StatusCode, GameMessage  

# Define some constants for card colors and types
COLORS = ["Red", "Green", "Blue", "Yellow"]
TYPES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw2"]

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234
MAX_PLAYERS = 2

# Global variables to store player information
players = []
player_turn = 0

# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(MAX_PLAYERS)
print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")

# Function to broadcast a message to all players
def broadcast(message):
    for player in players:
        data = pickle.dumps(GameMessage(StatusCode.NOTIFICATION, message))
        player.send(data)
        #player.send(message.encode(encoding='utf-8'))

# Function to handle a client
def handle_client(client_socket, turn):
    global player_turn
    while True:
        if turn == player_turn:
            try:
                
                data = pickle.dumps(GameMessage(StatusCode.IN_TURN, None))
                
                client_socket.send(data)
                
                data = client_socket.recv(1024)
                
                #reconstructed_data = pickle.loads(data)
                
                """
                if not data:
                    break
                """
                addr,port = client_socket.getpeername()
                
                m = f"{addr} : {port} played {data.decode('utf-8')}"
                
                print(m)
                # Broadcast the received card data to all players
                broadcast(m)
    
                # Move to the next player's turn
                player_turn = (player_turn + 1) % len(players)
            except:
                break

turn_assign = 0

# Accept and handle incoming connections
while len(players) < MAX_PLAYERS:
    client_socket, addr = server_socket.accept()
    players.append(client_socket)
    print(f"Player {len(players)} connected from {addr}")
    
    # Start a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, turn_assign))
    client_handler.start()
    turn_assign = turn_assign + 1 

server_socket.close()
