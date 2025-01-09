import tkinter as tk
from tkinter import scrolledtext
import threading
import socket

class SupportChatClient:
    def __init__(self, master, client_socket):
        self.master = master
        master.title("Support Chat Client")

        self.client_socket = client_socket

        self.chat_log = scrolledtext.ScrolledText(master, state='disabled')
        self.chat_log.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.client_socket.send(message.encode('utf-8'))
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, f"You: {message}\n")
        self.chat_log.config(state='disabled')
        self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_log.config(state='normal')
                self.chat_log.insert(tk.END, f"Server: {message}\n")
                self.chat_log.config(state='disabled')
            except ConnectionResetError:
                break

if __name__ == "__main__":
    root = tk.Tk()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    client = SupportChatClient(root, client_socket)
    root.mainloop()

