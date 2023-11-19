import socket
from status_code import StatusCode, UnoMessage
import pickle
import threading
import queue
import time
from card import CardColor, CardType 
from card_collections import UnoDeck

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234
#MAX_PLAYERS = 2

class Server:

    def __init__(self, num_players):
        # variables to store player information
        self.player_turn = 0
        self.players = []
        self.usernames = []
        self.pending_acknoledgements = []
        self.apply_card_effects = False
        self.game_won = False
        self.num_players = num_players
        
        # game variables
        self._deck = self._discarded_pile = None
        self.turn_increase = 1
        
        # Initialize the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER_IP, SERVER_PORT))
        self.server_socket.listen(self.num_players)
        print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")
        
    def run(self):
        # Accept and handle incoming connections
        while len(self.players) < self.num_players:
            client_socket, addr = self.server_socket.accept()
            self.players.append(client_socket)
            print(f"Player {len(self.players)} connected from {addr}")
            print(f"peer: {client_socket.getpeername()}")
            
            """
            # Start a new thread to handle the client
            client_handler = threading.Thread(target=handle_client_requests, args=(client_socket, turn_assign))
            client_handler.start()
            turn_assign = turn_assign + 1 
            """
        # Makes a list of player names
        for player in self.players:
            self.usernames.append(str(player.getpeername()))
        
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
            
            client_handler = threading.Thread(
                target=self.handle_client_requests, args=(player,))
            client_handler.start()
            
        # Starts first players turn          
        #self.next_turn()
            
    def broadcast(self, status_code, dta):
        for player in self.players:
            self.send_response(player, UnoMessage(
                status_code, dta))
            
    def next_turn(self):
        
        if not self.game_won:
            # Set next player's turn
            self.calc_player_turn()
            
            # Apply effects from discarded card
            if self.apply_card_effects:
                self.handle_card_effects()  
                self.apply_card_effects = False
        
        #client_socket = self.players[self.player_turn]
        # Sends the player in turn and a list of all players to all players
        #data = [self.player_turn, self.usernames]
        data = [self.player_turn, self.usernames,
                self.top_discarded_card(), self.game_won]
        
        #u_m = UnoMessage(StatusCode.GAME_STATE, data)
        self.broadcast(StatusCode.GAME_STATE, data)
        #self.send_response(client_socket, u_m)
            
    def handle_client_requests(self, client_socket):
        client_socket.settimeout(None)
        
        while True:
            try:
                
                if not self.pending_acknoledgements:
                    client_socket.settimeout(None)
                    
                request = client_socket.recv(4096)
                
                uno_msg = pickle.loads(request)
                
                self.handle_client_message(client_socket, uno_msg)
                
                """
                if self.pending_acknoledgements:
                    for pend_ack in self.pending_acknoledgements:
                        if (uno_msg.status_code == StatusCode.ACK and 
                            uno_msg.data == pend_ack.status_code):
                            self.pending_acknoledgements.remove(pend_ack)
                            """
                            
                if self.pending_acknoledgements:
                    uno_msg = self.pending_acknoledgements.pop(0)
                
            except socket.timeout:
                uno_msg = self.pending_acknoledgements.pop(0)
                self.send_response(client_socket, uno_msg)
                self.pending_acknoledgements.insert(0, uno_msg)
            except Exception as e:
                print(f'Error handling client request: {e}')
                break


    def handle_client_message(self, client_socket, uno_msg):   
        print(f'RECEIVING : {uno_msg.status_code}')
        status_code = uno_msg.status_code
        # send initial draw of cards to client
        if status_code == StatusCode.INITIAL_DRAW:
            card_list = []
            for i in range(7):
                uno_card = self.draw_from_deck()
                card_list.append(uno_card)
                
            u = UnoMessage(StatusCode.CARD_DRAW, card_list)
            self.send_response(client_socket, u)
            
        elif status_code == StatusCode.CARD_DRAW:
            uno_card = self.draw_from_deck()
            u = UnoMessage(StatusCode.CARD_DRAW, [uno_card])
            self.send_response(client_socket, u)
            self.next_turn()
            
        elif status_code == StatusCode.CARD_PLAY:
            card_played = uno_msg.data[0]
            self.game_won = uno_msg.data[1]
            self._discarded_pile.append(card_played)
            self.apply_card_effects = True
            #status_code = StatusCode.CARD_PLAY_NOTIFICATION
            #dta = [client_socket.getpeername(), self.top_discarded_card()]
            #self.broadcast(status_code, dta)
            #self.handle_card_effects(client_socket, self.top_discarded_card())
            self.next_turn()
            
        elif status_code == StatusCode.GAME_STATE:
            data = [self.player_turn, self.usernames,
                    self.top_discarded_card(), self.game_won]
            u = UnoMessage(StatusCode.GAME_STATE, data)        
            self.send_response(client_socket, u)   
            self.pending_acknoledgements.append(u)
            client_socket.settimeout(1)
            
        """
        elif status_code == StatusCode.DISCARD_CARD:
            uno_card = self.top_discarded_card()
            u = UnoMessage(StatusCode.DISCARD_CARD, uno_card)
            self.send_response(client_socket, u)
        """            
                
    def send_response(self, client_socket, uno_message):   
        r_dta = pickle.dumps(uno_message)
        print(f'SENDING : {uno_message.status_code}')
        client_socket.send(r_dta)        
        
    def handle_card_effects(self):  
        uno_card = self.top_discarded_card()
        if uno_card.type == CardType.SKIP:
            self.calc_player_turn()
            
        if uno_card.type == CardType.REVERSE:
            self.turn_increase *= -1
            self.calc_player_turn()
        
        if uno_card.type == CardType.DRAW_TWO:
            l = []
            c_s = self.players[self.player_turn]
            for i in range(2):
                l.append(self.draw_from_deck())
            uno_msg = UnoMessage(StatusCode.CARD_DRAW, l)
            self.send_response(c_s, uno_msg) 
            self.pending_acknoledgements.append(uno_msg)
            c_s.settimeout(1)
        
        if uno_card.type == CardType.WILD_DRAW_FOUR:
            l = []
            c_s = self.players[self.player_turn]
            for i in range(4):
                l.append(self.draw_from_deck())
            uno_msg = UnoMessage(StatusCode.CARD_DRAW, l)
            self.send_response(c_s, uno_msg)  
            self.pending_acknoledgements.append(uno_msg)
            c_s.settimeout(1)
        
            
    def top_discarded_card(self):  
        return self._discarded_pile[-1]          
    
    def calc_player_turn(self):  
        self.player_turn += self.turn_increase
        self.player_turn %= len(self.players)
        
    def draw_from_deck(self):
        if len(self._deck) == 0:
            for card in self._discarded_pile:
                self._deck.add(card)
        return self._deck.draw_card()
            
        
            
            
            
if __name__ == "__main__":
    num_players = 0
    # Make a game instance, and run the game.
    while num_players < 2 or num_players > 10:
        num_players = int(input(
            'Please input the amount of players(2-10) | inclusive: '))
    
    server = Server(num_players)
    server.run()    








        
            
        