import socket
from status_code import StatusCode, UnoResponse
import pickle
import threading
import queue
from card import CardColor, CardType 
from card_collections import UnoDeck

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234
MAX_PLAYERS = 1

class Server:

    def __init__(self):
        # variables to store player information
        self.player_turn = 0
        self.players = []
        
        # game variables
        self._deck = None
        
        # Initialize the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER_IP, SERVER_PORT))
        self.server_socket.listen(MAX_PLAYERS)
        print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")
        
    def run(self):
        turn_assign = 0
        
        # Accept and handle incoming connections
        while len(self.players) < MAX_PLAYERS:
            client_socket, addr = self.server_socket.accept()
            self.players.append(client_socket)
            print(f"Player {len(self.players)} connected from {addr}")
                        
            
            """
            # Start a new thread to handle the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket, turn_assign))
            client_handler.start()
            turn_assign = turn_assign + 1 
            """
        
        self.start_game()

        self.server_socket.close()        

    def start_game(self):
        self._deck = UnoDeck()
        self._deck.shuffle()
        # Tells all players game started
        for player in self.players:
            data = pickle.dumps(UnoResponse(StatusCode.GAME_START))
            player.send(data)
            
            client_handler = threading.Thread(target=self.handle_client_requests, args=(player,))
            client_handler.start()
       
        
    def broadcast(self, message):
        for player in self.players:
            data = pickle.dumps(UnoResponse(StatusCode.NOTIFICATION, message))
            player.send(data)
            #player.send(message.encode(encoding='utf-8'))    
            
            
    def handle_client_requests(self, client_socket):
        while True:
            request = client_socket.recv(1024)
            u_request = pickle.loads(request)
            r_status_code = u_request.status_code
            
            # send initial draw of cards to client
            if r_status_code == StatusCode.INITIAL_DRAW:
                card_list = []
                for i in range(7):
                    uno_card = self._deck.draw_card()
                    card_list.append(uno_card)
                    
                r = UnoResponse(StatusCode.INITIAL_DRAW, card_list)
                r_dta = pickle.dumps(r)
                client_socket.send(r_dta)  
                
            elif r_status_code == StatusCode.CARD_DRAW:
                uno_card = self._deck.draw_card()
                r = UnoResponse(StatusCode.CARD_DRAW, uno_card)
                r_dta = pickle.dumps(r)
                client_socket.send(r_dta)   
                
    def send_response(self, client_socket, r):   
        r_dta = pickle.dumps(r)
        client_socket.send(r_dta)               
            
if __name__ == "__main__":
    # Make a game instance, and run the game.
    server = Server()
    server.run()    








        
            
        