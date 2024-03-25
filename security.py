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
def get_session_key(hashed_pw):
    key = secrets.token_hex(16)
    aes_key = hashed_pw[:32].encode()
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_key = cipher.encrypt(pad(key.encode(), AES.block_size))
    return encrypted_key
def decrypt_key(encrypted_key, hashed_pw):
    key_for_decryption = hashed_pw[:32]
    cipher = AES.new(key_for_decryption, AES.MODE_ECB)
    decrypted_key = unpad(cipher.decrypt(encrypted_key), AES.block_size)
    return decrypted_key.decode