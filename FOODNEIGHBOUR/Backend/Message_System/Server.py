import socket
import threading

clients = []

def handle_client(client_socket, addr):
    print(f"Handling client {addr}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message.startswith("SUPPORT_REQUEST"):
                print("Support request received.")
                client_socket.send("SUPPORT_INITIATED".encode('utf-8'))
            else:
                print(f"Received from {addr}: {message}")
                client_socket.send(f"Message received: {message}".encode('utf-8'))
        except ConnectionResetError:
            break
    client_socket.close()
    clients.remove(client_socket)
    print(f"Connection with {addr} closed.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()

