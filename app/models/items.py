from operator import is_
import os
import pathlib

from tinydb import TinyDB, Query 
from dotenv import find_dotenv, load_dotenv
from app.utility import common
from app.config import constants
from google.cloud import storage
from app.utils import generate_download_signed_url_v4, move_blob

load_dotenv(find_dotenv())

client = storage.Client()

PATH_RESOURCES = os.getenv("PATH_RESOURCES")



def get_db(bucket_id, sub_bucket_id):
    bucket = bucket_id + "_" + str(sub_bucket_id)
    path_bucket = os.path.join(PATH_RESOURCES, "tdb", bucket+".json")
    db_bucket = TinyDB(path_bucket)
    return db_bucket

def add_item(bucket_id, sub_bucket_id, item):
    db_bucket = get_db(bucket_id, sub_bucket_id)
    db_bucket.insert(item)

def find_item_by_name(bucket_id, sub_bucket_id, name):
    db_bucket = get_db(bucket_id, sub_bucket_id)
    find = Query()
    item = db_bucket.search(find.name == name)
    return item

def list_item(bucket_id, sub_bucket_id, page, count_per_page):
    db_bucket = get_db(bucket_id, sub_bucket_id)
    items = db_bucket.all()
    if ((page*10) - (len(items))) < count_per_page  :
        st = (page * count_per_page) - count_per_page
        en = page * count_per_page
        return items[st:en]
    else:
        return []

def get_item(bucket_id, sub_bucket_id, itemid):
    db_bucket = get_db(bucket_id, sub_bucket_id)
    find = Query()
    item = db_bucket.search(find.id == itemid)
    return item

def update_item(bucket_id, sub_bucket_id, itemid, item_dict):
    db_bucket = get_db(bucket_id, sub_bucket_id)
    find = Query()
    db_bucket.update(item_dict, find.id == itemid)
    item = db_bucket.search(find.id == itemid)
    return item[0]


# HELPER FUNCTIONS
def get_item_by_page(list_items, bucket_id, limit, page_token, sub_bucket_id):
    prefix_raw = get_info(bucket_id,sub_bucket_id)
    bucket_name = get_bucket_name(bucket_id)
    print(prefix_raw)
    blob_list = client.list_blobs(bucket_name, max_results=limit, prefix=prefix_raw,
        fields='items(name,contentLanguage),nextPageToken', page_token=page_token)
    for page in blob_list.pages:
        for blob in list(page):
            if "." in blob.name:
                print(blob.name)
                exist_item = find_item_by_name(bucket_id, sub_bucket_id, blob.name)
                if len(exist_item) < 1:
                    tmp = {}
                    tmp["name"] = blob.name
                    tmp["id"] = str(common.generate_random())
                    tmp["status"] = True
                    tmp["signed_url"] = ""
                    tmp["flag"] = constants.TAGS['RAW']
                    add_item(bucket_id, sub_bucket_id, tmp)
                    list_items.append(tmp)
    return blob_list.next_page_token

def get_bucket_name(bucket_id):
    bucket_name = False
    if bucket_id in constants.dict_bucket.keys():
        bucket_name = constants.dict_bucket[bucket_id]["name"]
    return bucket_name

def move_item(bucket_id, sub_bucket_id, itemname, flag):
    is_move = constants.dict_bucket[bucket_id]["page"][sub_bucket_id]["is_move"]
    if is_move:
        itemname = itemname.split('/')[-1]
        srce_path = constants.dict_bucket[bucket_id]["page"][sub_bucket_id]["flag"][0]+ itemname
        dest_path = constants.dict_bucket[bucket_id]["page"][sub_bucket_id]["flag"][flag]+ itemname
        print(srce_path)
        print(dest_path)
        bucket_name = get_bucket_name(bucket_id)
        move_blob(bucket_name=bucket_name, blob_name=srce_path,
                                        destination_bucket_name=bucket_name, destination_blob_name=dest_path)


def get_info(bucket_id,sub_bucket_id):
    bucket = constants.dict_bucket[bucket_id]
    sub_bucket = bucket["page"][sub_bucket_id]
    raw_folder = sub_bucket["flag"][0]
    return raw_folder