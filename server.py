import socket
from status_code import StatusCode, UnoMessage
import pickle
import threading
from card import CardType 
from card_collections import UnoDeck

class Server:
    """
    Represents the Uno game server for handling multiplayer gameplay.
    """    
    LOCAL_IP_ADDRESS = '127.0.0.1'

    def __init__(self, server_address, port, num_players):
        """
        Initializes the Uno game server.

        Args:
            server_address (str): The IP address to bind the server.
            port (int): The port number for the server.
            num_players (int): Number of players in the game.
        """        
        # Game variables
        self.player_turn = 0
        self.players = []
        self.usernames = []
        self.pending_acknoledgements = []
        self.apply_card_effects = False
        self.game_won = False
        self.num_players = num_players
        host_address = Server.LOCAL_IP_ADDRESS
        
        self._deck = self._discarded_pile = None
        self.turn_increase = 1
        
        # Sets up server ip address
        if not host_address == server_address:
            host_address = '0.0.0.0'
        
        # Initialize the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host_address, port))
        self.server_socket.listen(self.num_players)
        print(f"\nServer is listening on {server_address}:{port}")
        
    def run(self):
        """
        Runs the server to accept and handle incoming connections.
        """        
        # Accept and handle incoming connections
        while len(self.players) < self.num_players:
            client_socket, addr = self.server_socket.accept()
            self.players.append(client_socket)
            print(f"Player {len(self.players)} connected from {addr}")
            print(f"peer: {client_socket.getpeername()}")
            
        # Makes a list of player names
        for player in self.players:
            self.usernames.append(str(player.getpeername()))
        
        self.start_game()

        self.server_socket.close()        

    def start_game(self):
        """
        Initializes the game state and notifies players that the game has started.
        """        
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
            
            
    def broadcast(self, status_code, dta):
        """
        Broadcasts a message to all connected players.

        Args:
            status_code (StatusCode): The status code of the message.
            data: The data to be sent to the players.
        """        
        for player in self.players:
            self.send_response(player, UnoMessage(
                status_code, dta))
            
    def next_turn(self):
        """
        Handles the transition to the next player's turn.
        """        
        if not self.game_won:
            # Set next player's turn
            self.calc_player_turn()
            
            # Apply effects from discarded card
            if self.apply_card_effects:
                self.handle_card_effects()  
                self.apply_card_effects = False
        
        # Sends the player in turn and a list of all players to all players
        data = [self.player_turn, self.usernames,
                self.top_discarded_card(), self.game_won]
        
        self.broadcast(StatusCode.GAME_STATE, data)
            
    def handle_client_requests(self, client_socket):
        """
        Handles incoming requests from a connected client.

        Args:
            client_socket (socket): The socket of the connected client.
        """        
        client_socket.settimeout(None)
        
        while True:
            try:
                # Resets timeouts if there are no pending acknoledgements
                if not self.pending_acknoledgements:
                    client_socket.settimeout(None)
                    
                request = client_socket.recv(512)
                
                # Deserializes message
                uno_msg = pickle.loads(request)
                
                self.handle_client_message(client_socket, uno_msg)
                            
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
        """
        Handles a message received from a connected client.

        Args:
            client_socket (socket): The socket of the connected client.
            uno_msg (UnoMessage): The UnoMessage received from the client.
        """        
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
            self.next_turn()
            
        elif status_code == StatusCode.GAME_STATE:
            data = [self.player_turn, self.usernames,
                    self.top_discarded_card(), self.game_won]
            u = UnoMessage(StatusCode.GAME_STATE, data)        
            self.send_response(client_socket, u)   
            self.pending_acknoledgements.append(u)
            client_socket.settimeout(1)

            
    def send_response(self, client_socket, uno_message):   
        """
        Sends a response to a connected client.

        Args:
            client_socket (socket): The socket of the connected client.
            uno_message (UnoMessage): The UnoMessage to be sent.
        """        
        r_dta = pickle.dumps(uno_message)
        print(f'SENDING : {uno_message.status_code}')
        client_socket.send(r_dta)        
        
    def handle_card_effects(self): 
        """
        Handles special effects of the discarded card.
        """        
        uno_card = self.top_discarded_card()
        
        # Skip
        if uno_card.type == CardType.SKIP:
            self.calc_player_turn()
            
        # Reverse
        if uno_card.type == CardType.REVERSE:
            self.turn_increase *= -1
            self.calc_player_turn()
        
        # +2 Card
        if uno_card.type == CardType.DRAW_TWO:
            l = []
            c_s = self.players[self.player_turn]
            for i in range(2):
                l.append(self.draw_from_deck())
            uno_msg = UnoMessage(StatusCode.CARD_DRAW, l)
            self.send_response(c_s, uno_msg) 
            self.pending_acknoledgements.append(uno_msg)
            c_s.settimeout(1)
        
        # +4 Card
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
        """
        Returns the top card from the discarded pile.
        """        
        return self._discarded_pile[-1]          
    
    def calc_player_turn(self):  
        """
        Calculates the next player's turn.
        """        
        self.player_turn += self.turn_increase
        self.player_turn %= len(self.players)
        
    def draw_from_deck(self):
        """
        Draws a card from the Uno deck.

        Returns:
            UnoCard: The drawn Uno card.
        """        
        if len(self._deck) == 0:
            for card in self._discarded_pile:
                self._deck.add(card)
        return self._deck.draw_card()
            
        
        
def get_local_ipv4():
    """
    Retrieves the local IPv4 address.

    Returns:
        str: The local IPv4 address.
    """    
    # Creates a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to any remote server (doesn't actually send data)
        s.connect(('8.8.8.8', 80))
        # Get the local IP address from the connected socket
        local_ip = s.getsockname()[0]
    except socket.error:
        local_ip = Server.LOCAL_IP_ADDRESS  # Default to localhost if unable to connect

    finally:
        # Close the socket
        s.close()   
        
    return local_ip
            
            
if __name__ == "__main__":
    """
    The main block for configuring and running the Uno game server.

    - Sets the server address based on user input.
    - Prompts the user to input the number of players for the game.
    - Creates a Server and runs it.
    """    
    # Server configuration
    # Sets server address 
    host_address_option = -1
    host_address = ""
    local_ipv4 = get_local_ipv4()
    local_address = Server.LOCAL_IP_ADDRESS
    
    while not host_address_option == 0 and not host_address_option == 1:
        host_address_option = int(input(
        (f'[0] Run the server on {local_ipv4} (IPv4)\n'
         '[1] Run the server on localhost\n'
         'Input 0 or 1: ')
        ))

    if host_address_option == 1:
        host_address = local_address
    else:
        host_address = local_ipv4
        
    # Sets the ammount of player that will play
    num_players = 0
    while num_players < 2 or num_players > 10:
        num_players = int(input(
            '\nInput the amount of players(2-10) | inclusive: '))
    
    # Make a game instance, and run the game.
    server = Server(host_address, 1234, num_players)
    server.run()    
