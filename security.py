import hashlib

def hash_pw(pw):
    hashed = hashlib.sha512(pw.encode()).hexdigest()
    return hashed
def check_pw(pw, hashed):
    return hashed == pw