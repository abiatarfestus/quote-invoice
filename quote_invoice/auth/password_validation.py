import bcrypt

def generate_password_hash(password):
    bytes = password.encode('utf-8') # converting password to array of bytes
    salt = bcrypt.gensalt() # generating the salt
    hash = bcrypt.hashpw(bytes, salt) # Hashing the password
    return hash


def check_password_hash(password, saved_password_hash):
    password = password.encode('utf-8') # encoding user password
    result = bcrypt.checkpw(password, saved_password_hash) # checking password
    return result