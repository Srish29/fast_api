from datetime import datetime, timedelta
from click import password_option
from fastapi import APIRouter, Request
from app.config import constants
from app.utility import common
from app.models import users
from app.oauth2 import create_access_token, verify_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = constants.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
@router.get("/user/health-check")
def health_check(request: Request,):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        dict_resp["status"] = True
        dict_resp["msg"] = "healthy"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.post("/user/auth")
def auth_user(req_user: dict):
    dict_resp = constants.default_response.copy()
    auth_user = req_user.copy()
    if common.validate_dict(auth_user, ["emailid", "password"]):
        exist_user = users.find_user_by_email(auth_user["emailid"])
        if len(exist_user) == 1:
            print(exist_user)
            hashed_password = exist_user[0]["hashed_password"]
            decrypt = common.verify_password(auth_user["password"], hashed_password)
            if decrypt:
                user_token = common.remove_key_from_dict(exist_user[0].copy(), ["hashed_password"])
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"user": user_token}, expires_delta=access_token_expires
                )
                token = {
                    "token": access_token,
                    "token_type": "jwt",
                    "expired_in_min": ACCESS_TOKEN_EXPIRE_MINUTES,
                }
                dict_resp["status"] = True
                dict_resp["msg"] = "User authorized."
                dict_resp["data"] = token
            else:
                dict_resp["msg"] = "Invalid password."
        else:
            dict_resp["msg"] = "Email id does not exist."
    else:
        dict_resp["msg"] = "Emailid and Password must not be empty"
    return dict_resp

@router.post("/user/add")
def add_user(request: Request, req_user: dict):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        user = req_user.copy()
        if common.validate_dict(user, ["emailid", "username", "password", "role"]):
            exist_user = users.find_user_by_email(user["emailid"])
            if len(exist_user) < 1:
                user["id"] = str(common.generate_random())
                user["hashed_password"] = common.encrypt(user["password"])
                del user['password']
                # user["decrypt"] = common.verify_password(user["password"], user["hashed_password"])
                user["status"] = "Active"
                user["created_by"] = "Admin"
                user["role"] = "Admin"
                user["bucketid"] = []
                user["created_on"] = datetime.now().isoformat()
                users.add_user(user)
                dict_resp["status"] = True
                dict_resp["msg"] = "User added."
                dict_resp["user"] = user["id"]
            else:
                dict_resp["msg"] = "Email id already exist."
        else:
            dict_resp["msg"] = "Name, Emailid, Password and Role must not be empty"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.get("/user/{id}")
def user_by_id(request: Request, id : str):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if id != "":
            exist_user = users.find_user(id)
            if len(exist_user) == 1:
                user = common.remove_key_from_dict(exist_user[0], ["hashed_password"])
                dict_resp["status"] = True
                dict_resp["msg"] = "User fetched."
                dict_resp["user"] = exist_user[0]
            else:
                dict_resp["msg"] = "User id does not exist."
        else:
            dict_resp["msg"] = "user id must not be empty"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.get("/user/email/{email}")
def user_by_email(request: Request, email : str):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if id != "":
            exist_user = users.find_user_by_email(email)
            if len(exist_user) == 1:
                user = common.remove_key_from_dict(exist_user[0], ["hashed_password"])
                dict_resp["status"] = True
                dict_resp["msg"] = "User fetched."
                dict_resp["user"] = exist_user[0]
            else:
                dict_resp["msg"] = "Email id does not exist."
        else:
            dict_resp["msg"] = "email id must not be empty"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.delete("/user/{id}")
def delete_user(request: Request, id : str):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if id != "":
            exist_user = users.find_user(id)
            if len(exist_user) == 1:
                is_deleted = users.delete_user(id)
                if is_deleted:
                    dict_resp["status"] = True
                    dict_resp["msg"] = "User deleted."
                else:
                    dict_resp["msg"] = "Try again"
            else:
                dict_resp["msg"] = "User id does not exist."
        else:
            dict_resp["msg"] = "user id must not be empty"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.post("/user/{type}/bucket")
def delete_user(request: Request, type : str, req_user: dict):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if type in ['add','remove']:
            exist_user = users.find_user_by_email(req_user['emailid'])
            if len(exist_user) == 1:
                if req_user['bucketid'] in constants.dict_bucket.keys():
                    isupdated = users.upadte_bucket(req_user['emailid'],req_user['bucketid'],type)
                    if isupdated:
                        dict_resp["status"] = True
                        dict_resp["msg"] = "Bucket updated to user."
                    else:
                        dict_resp["msg"] = "try again."
                else:
                    dict_resp["msg"] = "bucket id does not exist."
            else:
                dict_resp["msg"] = "User email id does not exist."
        else:
            dict_resp["msg"] = "invalid url"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

#note

# 2. update user
# 3. change password
# 4. reset password 
