import socket
import threading
import json
import datetime
import sys
from colorama import Fore, init

init(autoreset=True)

# === Banner ===
banner = f"""{Fore.CYAN}


╔══════════════════════════════════╗
║           ChatServer             ║
╚══════════════════════════════════╝


   {Fore.YELLOW}Welcome to ChatServer
   Type '/shutdown' in this window to shut down the server.
"""

print(banner)

# === Server setup ===
host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

shutdown_flag = threading.Event()

# === Broadcast messages ===
def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                pass

# === Handle each client ===
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            decoded = message.decode('utf-8')

            if decoded == '/quit':
                index = clients.index(client)
                nickname = nicknames[index]
                timestamp = datetime.datetime.now().strftime('%H:%M')
                leave_msg = f"{Fore.RED}[{timestamp}] {nickname} has left the chat."
                print(leave_msg)
                broadcast(leave_msg.encode('utf-8'), client)
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                break

            else:
                print(decoded)
                broadcast(message, client)

        except:
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                timestamp = datetime.datetime.now().strftime('%H:%M')
                crash_msg = f"{Fore.RED}[{timestamp}] {nickname} disconnected unexpectedly."
                print(crash_msg)
                broadcast(crash_msg.encode('utf-8'))
            break

# === Accept connections ===
def receive():
    while not shutdown_flag.is_set():
        try:
            client, address = server.accept()
            nickname = client.recv(1024).decode('utf-8')

            # 🔁 Reload users.json every time a new client connects
            with open('users.json', 'r') as f:
                valid_users = json.load(f)

            # Authenticate nickname
            if nickname not in valid_users:
                client.send("/quit".encode('utf-8'))
                client.close()
                print(f"{Fore.RED}Connection rejected from {address} - Unknown user: {nickname}")
                continue

            clients.append(client)
            nicknames.append(nickname)

            timestamp = datetime.datetime.now().strftime('%H:%M')
            print(f"{Fore.GREEN}[{timestamp}] {nickname} joined from {address}")
            broadcast(f"{Fore.YELLOW}[{timestamp}] {nickname} joined the chat.".encode('utf-8'), client)
            client.send(f"{Fore.CYAN}Welcome to the chat, {nickname}!".encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            break

# === Server shutdown input handler ===
def listen_for_shutdown():
    while True:
        cmd = input()
        if cmd.strip() == '/shutdown':
            shutdown_flag.set()
            print(f"{Fore.RED}Server is shutting down...")
            for client in clients:
                try:
                    client.send("/quit".encode('utf-8'))
                    client.close()
                except:
                    pass
            server.close()
            sys.exit()

# === Launching ===
accept_thread = threading.Thread(target=receive)
accept_thread.start()

shutdown_thread = threading.Thread(target=listen_for_shutdown)
shutdown_thread.start()

