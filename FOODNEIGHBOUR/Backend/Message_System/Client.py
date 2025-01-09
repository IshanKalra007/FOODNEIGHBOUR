import socket
import tkinter as tk
from SupportChatGUI import SupportChatClient

def request_support():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    client_socket.send("SUPPORT_REQUEST".encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "SUPPORT_INITIATED":
        root = tk.Tk()
        client = SupportChatClient(root, client_socket)
        root.mainloop()
    else:
        print("Failed to initiate support.")
    client_socket.close()

if __name__ == "__main__":
    request_support()
