# worker.py
import socket
import time
import threading

def handle_request(connection, address, app_type):
    if app_type == "Long":
        print(f"[Worker] Processing long request from {address}")
        time.sleep(5)  # Simulate a long computation
    elif app_type == "Short":
        print(f"[Worker] Processing short request from {address}")
        time.sleep(1)  # Simulate a short computation
    connection.sendall(b"Response from Worker")
    connection.close()

def worker_server(port, worker_id):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen()
    print(f"[Worker-{worker_id}] Listening on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        data = conn.recv(1024).decode()
        app_type = data.split(":")[1].strip()
        threading.Thread(target=handle_request, args=(conn, addr, app_type)).start()

if __name__ == "__main__":
    import sys
    worker_id = sys.argv[1]
    worker_port = 9001 + int(worker_id)
    worker_server(worker_port, worker_id)
