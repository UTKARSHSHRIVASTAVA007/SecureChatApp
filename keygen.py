from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Your shared secret key:\n{key.decode()}")

