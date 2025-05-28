# 💬 ChatRoom - A Secure Terminal Chat App

Welcome to **ChatRoom**, a terminal-based encrypted chat application built in Python using TCP sockets. It features user authentication, AES encryption, multi-user chat support, timestamps, and a CLI-friendly interface — perfect for privacy-conscious users who love working in the terminal.

---

## 🔐 Features

- ✅ **User Authentication** (JSON-based)
- 🔒 **End-to-End Encryption** using `cryptography`'s Fernet
- 🧠 **Password Hashing** using bcrypt
- ⌛ **Timestamps** for all messages
- 🎨 **Color-coded Messages** for better readability
- 🔄 **Server Shutdown Command**
- 💡 **Banner Messages & CLI Help**
- 📄 **Logging Optional** (not enabled by default)

## 🖥️ Usage
▶️ Start the Server
(python3 server.py)

▶️ Start the ChatRoom
(python3 client.py)

##🧪 First-time Setup
(python3 keygen.py)
[NOTE: This creates a secret.key file. Keep this safe and never upload it to GitHub! :)]

##📢 Commands

/quit — Disconnect from the chat

/shutdown — (Server only) Shut down the chat server


##⚠️ Security Notes

>Passwords are hashed with bcrypt, not stored in plain text.

>Messages are encrypted using Fernet (AES-128).

>Avoid pushing secret.key and users.json to public repositories.

>.gitignore is configured to protect sensitive files.

##Acknowledgements

Python Standard Library (socket, threading, datetime)

cryptography

bcrypt

colorama

---

## 🧰 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
