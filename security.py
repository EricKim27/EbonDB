import hashlib
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

def hash_pw(pw):
    hashed = hashlib.sha512(pw.encode()).hexdigest()
    return hashed
def check_pw(pw, hashed):
    return hashed == pw
# encryption class
# This class is for defining the encryption layer.
# It uses AES for encrypting. It encrypts the session key generated for each connection, and sends it to the client.
# Then the client and server use the session key to encrypt their data. 
# It is done like this so that the session key that is used for encrypting data is safely transmitted.
class encryption:
    def __init__(self):
        self.session_key = self.get_session_key()
    def get_session_key(self):
        return secrets.token_hex(16)
    def encrypt_session_key(self, hashed_pw):
        aes_key = hashed_pw[:32].encode()
        cipher = AES.new(aes_key, AES.MODE_CBC)
        encrypted_key = cipher.encrypt(pad(self.session_key.encode(), AES.block_size))
        return encrypted_key
    def decrypt_key(self, encrypted_key, hashed_pw):
        key_for_decryption = hashed_pw[:32]
        cipher = AES.new(key_for_decryption, AES.MODE_CBC)
        decrypted_key = unpad(cipher.decrypt(encrypted_key), AES.block_size)
        return decrypted_key.decode
    def encrypt_data(self, data):
        aes_key = self.session_key[:32].encode()
        cipher = AES.new(aes_key, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        return encrypted_data