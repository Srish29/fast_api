import os
import pathlib

from tinydb import TinyDB, Query 
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())



PATH_RESOURCES = os.getenv("PATH_RESOURCES")
path_users = os.path.join(PATH_RESOURCES, "tdb", "users.json")
db_users = TinyDB(path_users)

def add_user(user):
    db_users.insert(user)
    return "db"

def find_user_by_email(email):
    find = Query()
    user = db_users.search(find.emailid == email)
    return user

def find_user(id):
    find = Query()
    user = db_users.search(find.id == id)
    return user

def delete_user(id):
    find = Query()
    return db_users.remove(find.id == id)

def delete_user_by_email(id):
    db_users.insert(id)
    return "db"

def upadte_bucket(email,bucketid,type):
    user_dict = find_user_by_email(email)[0]
    if 'bucketid' in user_dict.keys():
        list_bucket = user_dict['bucketid']
        if type == 'add':
            if bucketid not in list_bucket:
                list_bucket.append(bucketid)
                user_dict['bucketid'] = list_bucket
        else:
            if bucketid in list_bucket:
                list_bucket.remove(bucketid)
                user_dict['bucketid'] = list_bucket
    else:
        list_bucket = []
        if type == 'add':
            list_bucket.append(bucketid)
            user_dict['bucketid'] = list_bucket
    find = Query()
    db_users.update(user_dict, find.emailid == email)
    return True