import socket
from status_code import StatusCode, UnoMessage
import pickle
import threading
import queue

class Client:
    """
    Represents a client in the Uno game application, responsible for 
        communication with the server.
    """    
    def __init__(self):
        """
        Initializes the Client instance.
        """        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.result_q = queue.Queue()
        self.pending_responses = []
                
    def connect_to_server(self, server_address, server_port):
        """
        Initiates a connection to the Uno server.

        Args:
            server_address (str): The IP address of the Uno server.
            server_port (int): The port number of the Uno server.
        """        
        self.server_address = server_address
        self.server_port = server_port
        connection_thread = threading.Thread(target=self.connection_attempt)
        connection_thread.start()   
            
    def connection_attempt(self):
        """
        Handles the connection attempt to the Uno server in a separate thread.
        """        
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            self.is_connected = True
            self.name = str(self.client_socket.getsockname())
            r = UnoMessage(StatusCode.CONNECTION_SUCCESS)
            
            # Client starts handling server responses
            game_thread = threading.Thread(target=self.handle_responses)
            game_thread.start()  
        except Exception as e:
            print(f'{e}')
            r = UnoMessage(StatusCode.CONNECTION_FAILED)
        
        self.result_q.put(r)
        
    def get_response(self):
        """
        Retrieves a response from the server.

        Returns:
            UnoMessage: The received UnoMessage from the server.
        """        
        r = self.result_q.get()
        print(f'RECEIVING : {r.status_code}\n')
        return r
    
    def response_received(self):
        """
        Checks if there are any pending responses in the result queue.

        Returns:
            bool: True if there are pending responses, False otherwise.
        """        
        return not self.result_q.empty()    
            
    def handle_responses(self):
        """
        Handles and processes incoming responses from the server.
        """        
        while self.is_connected:
            
            try:
                if not self.pending_responses:
                    self.client_socket.settimeout(None)
                
                response = self.client_socket.recv(512)
                uno_response = pickle.loads(response) 
                self.result_q.put(uno_response)
                
                if self.pending_responses:
                    self.pending_responses.pop(0)
                
            except socket.timeout:
                uno_msg = self.pending_responses.pop(0)
                self.send_request(uno_msg.status_code, uno_msg.data)
                
            except Exception as e:
                print(f'Receiving Exception: {e}\n')
        
    def request_initial_cards(self):
        """
        Sends a request to the server for initial card drawing.
        """        
        self.send_request(StatusCode.INITIAL_DRAW)  
        
    def request_card_draw(self):
        """
        Sends a request to the server to draw a card.
        """        
        self.send_request(StatusCode.CARD_DRAW)  
        
    def request_card_play(self, uno_card, is_winning_card):
        """
        Sends a request to the server to play a card.

        Args:
            uno_card: The Uno card to be played.
            is_winning_card (bool): Flag indicating whether the played card 
                leads to a win.
        """        
        self.send_request(StatusCode.CARD_PLAY, [uno_card, is_winning_card])

    def request_game_status(self):
        """
        Sends a request to the server for the current game state.
        """        
        self.send_request(StatusCode.GAME_STATE)        

    def request_win(self):
        """
        Sends a request to the server indicating a win.
        """        
        self.send_request(StatusCode.WIN)                          
        
    def send_request(self, status_code, dta=None):
        """
        Sends a request to the server with a given status code and optional data.

        Args:
            status_code: The status code of the request.
            dta: Optional data associated with the request.
        """        
        uno_msg = UnoMessage(status_code, dta)
        print(f'SENDING : {uno_msg.status_code}\n')
        
        try:
            # Serializes data with pickle
            serialized_msg = pickle.dumps(uno_msg)
            self.client_socket.send(serialized_msg) 
            self.pending_responses.insert(0, uno_msg)
            self.client_socket.settimeout(1)
            
        except socket.error as se:
            print(f"Socket error during send: {se}")
        except Exception as e:
            print(f"Unexpected error during send: {e}")     
            
    def close_connection(self):
        """
        Closes the connection with the Uno server.
        """        
        if self.is_connected:
            self.client_socket.close()
            self.is_connected = not self.is_connected
    