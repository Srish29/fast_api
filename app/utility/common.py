import uuid
import bcrypt

def generate_random():
    return uuid.uuid1()

def validate_dict(dict, list_key):
    flag = True
    for key in list_key:
        if key not in dict:
            flag = False
        else:
            if dict[key] == "":
                flag = False
    return flag

def remove_key_from_dict(dict, list_key):
    for key in list_key:
        if key in dict:
            del dict[key]
    return dict

# the salt is saved into the hash itself
def encrypt(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(password.encode(), hashed_password.encode('utf-8'))

def get_token(request, type):
    token = request.headers.get('Authorization')
    if token:
        token = token.replace(type, "").replace(" ", "")
    return token