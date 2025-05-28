import socket
import threading
from colorama import Fore, init
import datetime
import sys
import auth
from secret_key import fernet

init(autoreset=True)

banner = f"""{Fore.CYAN}


   ____  _             _     ____                          
  / ___|| |__    __ _ | |_  |  _ \  ___    ___   _ __ ___  
 | |    | '_ \  / _` || __| | |_) |/ _ \  / _ \ | '_ ` _ \ 
 | |___ | | | || (_| || |_  |  _ <| (_) || (_) || | | | | |
  \____||_| |_| \__,_| \__| |_| \_\\___/  \___/ |_| |_| |_|
                                                                                                  

            Welcome to the {Fore.GREEN}ChatRoom!

{Fore.YELLOW}Rules:
1. Be respectful.
2. No spamming.
3. Use '/quit' to leave the chat.

{Fore.MAGENTA}Type your messages below:
"""

print(banner)

def get_authenticated_username():
    while True:
        print("1. Login\n2. Signup\n3. Quit")
        choice = input("Select option: ").strip()
        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            success, msg = auth.login(username, password)
            print(msg)
            if success:
                return username
        elif choice == '2':
            username = input("Choose username: ").strip()
            password = input("Choose password: ").strip()
            success, msg = auth.signup(username, password)
            print(msg)
            if success:
                return username
        elif choice == '3':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option.")

nickname = get_authenticated_username()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
client.send(nickname.encode('utf-8'))

def receive():
    while True:
        try:
            encrypted = client.recv(1024)
            message = fernet.decrypt(encrypted).decode('utf-8')
            if message == '/quit':
                print("Disconnected by server.")
                client.close()
                break
            print(message)
        except:
            print("Error in connection.")
            client.close()
            break

def write():
    while True:
        msg = input()
        if msg.strip() == '/quit':
            client.send(fernet.encrypt('/quit'.encode('utf-8')))
            client.close()
            break
        timestamp = datetime.datetime.now().strftime('%H:%M')
        full_msg = f"{Fore.GREEN}[{timestamp}] {nickname}: {msg}"
        client.send(fernet.encrypt(full_msg.encode('utf-8')))

threading.Thread(target=receive).start()
threading.Thread(target=write).start()

