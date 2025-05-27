import socket
import threading
from colorama import Fore, init
import datetime
import sys
from utils import auth

init(autoreset=True)

# === Banner & Help ===
banner = f"""{Fore.CYAN}
╔══════════════════════════════════╗
║          ChatRoom                ║
╚══════════════════════════════════╝
Welcome to ChatRoom!

{Fore.YELLOW}Rules:
1. Be respectful.
2. No spamming.
3. Use '/quit' to leave the chat.

{Fore.MAGENTA}Type your messages below:
"""

print(banner)

# === Authentication Loop ===
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

# === Connect to Server ===
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Send nickname to server
client.send(nickname.encode('utf-8'))

# === Receive Thread ===
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '/quit':
                print("Disconnected by server.")
                client.close()
                break
            print(message)
        except:
            print("Error in connection.")
            client.close()
            break

# === Write Thread ===
def write():
    while True:
        msg = input()
        if msg.strip() == '/quit':
            client.send('/quit'.encode('utf-8'))
            client.close()
            break
        timestamp = datetime.datetime.now().strftime('%H:%M')
        full_msg = f"{Fore.GREEN}[{timestamp}] {nickname}: {msg}"
        client.send(full_msg.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

