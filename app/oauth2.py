from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from dotenv import find_dotenv, load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("TOKEN")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: str = payload.get("user")
        if user is None:
            return False
        else:
            return True
    except:
        return False

def verify_bucket_access(token: str, bucket_id):
    is_access = False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: dict = payload.get("user")
        if user:
            if "bucketid" in user.keys():
                if bucket_id in user["bucketid"]:
                    is_access = True
    except:
        is_access = False
    return is_access