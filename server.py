import socket
import threading
import json
import datetime
import sys
from colorama import Fore, init
from secret_key import fernet  # encryption
init(autoreset=True)

banner = f"""{Fore.CYAN}


   ____  _             _     ____                                
  / ___|| |__    __ _ | |_  / ___|   ___  _ __ __   __ ___  _ __ 
 | |    | '_ \  / _` || __| \___ \  / _ \| '__|\ \ / // _ \| '__|
 | |___ | | | || (_| || |_   ___) ||  __/| |    \ V /|  __/| |   
  \____||_| |_| \__,_| \__| |____/  \___||_|     \_/  \___||_|   
                                                                                                                                        

   {Fore.YELLOW}Welcome to ChatServer
   Type '/shutdown' in this window to shut down the server.
   
   (Made with <3 by - Utkarsh Shrivastava)
   
"""

print(banner)

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

shutdown_flag = threading.Event()

def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                encrypted = fernet.encrypt(message)
                client.send(encrypted)
            except:
                pass

def handle(client):
    while True:
        try:
            encrypted = client.recv(1024)
            message = fernet.decrypt(encrypted).decode('utf-8')

            if message == '/quit':
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
                print(message)
                broadcast(message.encode('utf-8'), client)

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

def receive():
    while not shutdown_flag.is_set():
        try:
            client, address = server.accept()
            nickname = client.recv(1024).decode('utf-8')

            with open('users.json', 'r') as f:
                valid_users = json.load(f)

            if nickname not in valid_users:
                client.send(fernet.encrypt("/quit".encode('utf-8')))
                client.close()
                print(f"{Fore.RED}Connection rejected from {address} - Unknown user: {nickname}")
                continue

            clients.append(client)
            nicknames.append(nickname)

            timestamp = datetime.datetime.now().strftime('%H:%M')
            print(f"{Fore.GREEN}[{timestamp}] {nickname} joined from {address}")
            join_msg = f"{Fore.YELLOW}[{timestamp}] {nickname} joined the chat."
            broadcast(join_msg.encode('utf-8'), client)
            client.send(fernet.encrypt(f"{Fore.CYAN}Welcome to the chat, {nickname}!".encode('utf-8')))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            break

def listen_for_shutdown():
    while True:
        cmd = input()
        if cmd.strip() == '/shutdown':
            shutdown_flag.set()
            print(f"{Fore.RED}Server is shutting down...")
            for client in clients:
                try:
                    client.send(fernet.encrypt("/quit".encode('utf-8')))
                    client.close()
                except:
                    pass
            server.close()
            sys.exit()

threading.Thread(target=receive).start()
threading.Thread(target=listen_for_shutdown).start()

