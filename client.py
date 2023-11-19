import socket
from status_code import StatusCode, UnoMessage
import pickle
import threading
import queue
import time

class Client:
    
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.result_q = queue.Queue()
        self.pending_responses = []
                
    def connect_to_server(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        connection_thread = threading.Thread(target=self.connection_attempt)
        connection_thread.start()   
            
    def connection_attempt(self):
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            self.is_connected = True
            self.name = str(self.client_socket.getsockname())
            #self.ip = self.name[0]
            #self.port = self.name[1]
            r = UnoMessage(StatusCode.CONNECTION_SUCCESS)
            #print(self.client_socket.getsockname())
            #print(self.client_socket.getpeername())
            
            # Client starts handling server responses
            game_thread = threading.Thread(target=self.handle_responses)
            game_thread.start()  
        except Exception as e:
            print(f'{e}')
            
            """
            if hasattr(e, 'code'):
                print(f"Error Code: {e.code}")
            """
            r = UnoMessage(StatusCode.CONNECTION_FAILED)
        
        self.result_q.put(r)
        
    def get_response(self):
        r = self.result_q.get()
        print(f'RECEIVING : {r.status_code}\n')
        return r
    
    def response_received(self):
        return not self.result_q.empty()    
            
    def handle_responses(self):
        while self.is_connected:
            
            try:
                if not self.pending_responses:
                    self.client_socket.settimeout(None)
                
                response = self.client_socket.recv(4096)
                uno_response = pickle.loads(response) 
                self.result_q.put(uno_response)
                
                if self.pending_responses:
                    self.pending_responses.pop(0)
                #self.send_acknoledgement(uno_response)

                
            except socket.timeout:
                uno_msg = self.pending_responses.pop(0)
                self.send_request(uno_msg.status_code, uno_msg.data)
                
            except Exception as e:
                print(f'Receiving Exception: {e}\n')
                #pass
                    #
                    
                #print(f'BLOCKING ERROR: {e}')
                #pass
        #self.client_socket.close()

        
    def request_initial_cards(self):
        self.send_request(StatusCode.INITIAL_DRAW)  
        
    def request_card_draw(self):
        self.send_request(StatusCode.CARD_DRAW)  
        
    def request_card_play(self, uno_card, is_winning_card):
        self.send_request(StatusCode.CARD_PLAY, [uno_card, is_winning_card])

    def request_game_status(self):
        self.send_request(StatusCode.GAME_STATE)        

    def request_win(self):
        self.send_request(StatusCode.WIN)                          
        
    def send_request(self, status_code, dta=None):
        uno_msg = UnoMessage(status_code, dta)
        print(f'SENDING : {uno_msg.status_code}\n')
        
        try:
            serialized_msg = pickle.dumps(uno_msg)
            self.client_socket.send(serialized_msg) 
            self.pending_responses.insert(0, uno_msg)
            self.client_socket.settimeout(1)
            
        except socket.error as se:
            print(f"Socket error during send: {se}")
        except Exception as e:
            print(f"Unexpected error during send: {e}")     
            
    def close_connection(self):
        if self.is_connected:
            self.client_socket.close()
            self.is_connected = not self.is_connected
            
    def send_acknoledgement(self, uno_msg):
            ack_msg = UnoMessage(StatusCode.ACK, uno_msg.status_code)
            serialized_msg = pickle.dumps(ack_msg)
            self.client_socket.send(serialized_msg)           
    
    