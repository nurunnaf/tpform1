import socket
import threading

# Worker Server Configurations
WORKER_ADDRESSES = [("localhost", 9002), ("localhost", 9003), ("localhost", 9004)]
worker_connections = [0, 0, 0]  # Track the load of each worker

def select_worker(approach):
    if approach == "least_connections":
        # Find the worker with the least connections
        return worker_connections.index(min(worker_connections))
    elif approach == "round_robin":
        # Find the worker based on round-robin approach
        select_worker.counter = (select_worker.counter + 1) % len(WORKER_ADDRESSES)
        return select_worker.counter

select_worker.counter = -1

def broker_server():
    broker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    broker_socket.bind(('localhost', 8000))
    broker_socket.listen()
    print("[Broker] Listening on port 8000...")

    while True:
        client_conn, client_addr = broker_socket.accept()
        print(f"[Broker] Connected with {client_addr}")
        data = client_conn.recv(1024).decode()
        app_type = data.split(":")[1].strip()

        approach = data.split(":")[2].strip()
        worker_id = select_worker(approach)
        worker_host, worker_port = WORKER_ADDRESSES[worker_id]

        try:
            worker_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            worker_conn.connect((worker_host, worker_port))
            worker_conn.sendall(f"AppID:{app_type}".encode())

            response = worker_conn.recv(1024)
            print(f"[Broker] Response from Worker-{worker_id + 1}: {response.decode()}")
            client_conn.sendall(response)
            
            # Update connection counter based on approach
            worker_connections[worker_id] += 1 if approach == "least_connections" else 0
            
        except ConnectionError:
            print(f"[Broker] Failed to connect to Worker-{worker_id + 1}")

        client_conn.close()
        worker_conn.close()

if __name__ == "__main__":
    broker_server()
