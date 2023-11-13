import socket
from status_code import StatusCode, UnoResponse, UnoRequest
import pickle
import threading
import queue

class Client:
    
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.result_q = queue.Queue()
        
    def connect_to_server(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        connection_thread = threading.Thread(target=self.connection_attempt)
        connection_thread.start()   
            
    def connection_attempt(self):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            self.is_connected = True
            r = UnoResponse(StatusCode.CONNECTION_SUCCESS)
            
            # Client starts handling server responses
            game_thread = threading.Thread(target=self.handle_responses)
            game_thread.start()  
        except Exception as e:
            print(f'{e}')
            
            """
            if hasattr(e, 'code'):
                print(f"Error Code: {e.code}")
            """
            r = UnoResponse(StatusCode.CONNECTION_FAILED)
        
        self.result_q.put(r)
        
    def get_response(self):
        return self.result_q.get()
    
    def response_received(self):
        return not self.result_q.empty()    
            
    def handle_responses(self):
        while self.is_connected:
            response = self.client_socket.recv(1024)
            uno_response = pickle.loads(response) 
            
            """
            data = pickle.dumps(StatusCode.IN_TURN)
                        
            client_socket.send(data)
                        
            data = client_socket.recv(1024)
                        
            reconstructed_data = pickle.loads(data)    
            """
            if uno_response.status_code == StatusCode.GAME_START:
                self.result_q.put(uno_response)
            elif uno_response.status_code == StatusCode.INITIAL_DRAW:
                self.result_q.put(uno_response)
            elif uno_response.status_code == StatusCode.CARD_DRAW:
                self.result_q.put(uno_response)                
            elif uno_response.status_code == StatusCode.IN_TURN:
                # Get card color and type from the user
                card_color = input("Enter card color (Red, Green, Blue, Yellow): ")
                card_type = input("Enter card type (0-9, Skip, Reverse, Draw2): ")
            
                # Send the card data to the server
                card_data = f"{card_color} {card_type}"
                self.client_socket.send(card_data.encode('utf-8'))
            elif uno_response.status_code == StatusCode.NOTIFICATION:
                print(uno_response.data)     
    
        self.client_socket.close()
        
    def request_initial_cards(self):
        self.send_request(StatusCode.INITIAL_DRAW)  
        
    def request_card_draw(self):
        self.send_request(StatusCode.CARD_DRAW)     
        
    def send_request(self, status_code):
        u_r = pickle.dumps(UnoRequest(status_code))
        self.client_socket.send(u_r)          
        
        
        
        
    
    