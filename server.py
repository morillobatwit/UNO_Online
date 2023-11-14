import socket
from status_code import StatusCode, UnoMessage
import pickle
import threading
import queue
from card import CardColor, CardType 
from card_collections import UnoDeck

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234
MAX_PLAYERS = 2

class Server:

    def __init__(self):
        # variables to store player information
        self.player_turn = 0
        self.players = []
        
        # game variables
        self._deck = self._discarded_pile = None
        self.turn_increase = 1
        
        # Initialize the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER_IP, SERVER_PORT))
        self.server_socket.listen(MAX_PLAYERS)
        print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")
        
    def run(self):
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
        
        self._discarded_pile = []
        self._discarded_pile.append(self._deck.draw_card())
        
        # Tells all players game started
        for player in self.players:
            data = pickle.dumps(UnoMessage(StatusCode.GAME_START))
            player.send(data)
            
            client_handler = threading.Thread(target=self.handle_client_requests, args=(player,))
            client_handler.start()
            
        
        # Tells first player it is his turn            
        self.next_turn()
            
    def broadcast(self, dta):
        for player in self.players:
            self.send_response(player, UnoMessage(
                StatusCode.CARD_PLAY_NOTIFICATION, dta))
            #player.send(data)
            #player.send(message.encode(encoding='utf-8'))    
            
    def next_turn(self):
        c_s = self.players[self.player_turn]
        u_m = UnoMessage(StatusCode.IN_TURN)
        self.send_response(c_s, u_m)
        
        # Set next player's turn
        self.calc_player_turn()
        
            
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
                    
                r = UnoMessage(StatusCode.INITIAL_DRAW, card_list)
                r_dta = pickle.dumps(r)
                client_socket.send(r_dta)
                
            elif r_status_code == StatusCode.CARD_DRAW:
                uno_card = self._deck.draw_card()
                r = UnoMessage(StatusCode.CARD_DRAW, [uno_card])
                r_dta = pickle.dumps(r)
                client_socket.send(r_dta)
                self.next_turn()
                
            elif r_status_code == StatusCode.DISCARD_CARD:
                uno_card = self.top_discarded_card()
                u = UnoMessage(StatusCode.DISCARD_CARD, uno_card)
                self.send_response(client_socket, u)
                
            elif r_status_code == StatusCode.CARD_PLAY:
                print(f'broadcasting {u_request.data.type} : {u_request.data.color} ')
                self._discarded_pile.append(u_request.data)
                self.broadcast([client_socket.getpeername(), 
                                self.top_discarded_card()])
                self.handle_card_effects(self.top_discarded_card())
                self.next_turn()
                
    def send_response(self, client_socket, uno_message):   
        r_dta = pickle.dumps(uno_message)
        client_socket.send(r_dta)        
        
    def handle_card_effects(self, uno_card):  
        if uno_card.type == CardType.SKIP:
            self.calc_player_turn()
        if uno_card.type == CardType.DRAW_TWO:
            l = []
            c_s = self.players[self.player_turn]
            for i in range(2):
                l.append(self._deck.draw_card())
            r = UnoMessage(StatusCode.CARD_DRAW, l)
            self.send_response(c_s, r) 
        if uno_card.type == CardType.REVERSE:
            self.turn_increase *= -1
            self.calc_player_turn()       
        if uno_card.type == CardType.WILD_DRAW_FOUR:
            l = []
            c_s = self.players[self.player_turn]
            for i in range(4):
                l.append(self._deck.draw_card())
            r = UnoMessage(StatusCode.CARD_DRAW, l)
            self.send_response(c_s, r)               
            
    def top_discarded_card(self):  
        return self._discarded_pile[-1]          
    
    def calc_player_turn(self):  
        self.player_turn += self.turn_increase
        self.player_turn %= len(self.players)
        
            
            
            
if __name__ == "__main__":
    # Make a game instance, and run the game.
    server = Server()
    server.run()    








        
            
        