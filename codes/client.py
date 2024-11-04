
import socket
import sys

def send_request(application_id, approach):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client_socket.connect(('localhost', 8000)) 
    message = f"AppID:{application_id}:{approach}" 
    client_socket.sendall(message.encode()) 

    response = client_socket.recv(1024) 
    print(f"[Client] Received: {response.decode()}") 
    client_socket.close() 

if __name__ == "__main__":
    application_id = sys.argv[1]  
    approach = sys.argv[2]       
    send_request(application_id, approach)  
