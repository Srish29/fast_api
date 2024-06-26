from datetime import datetime, timedelta
from fastapi import APIRouter, Request
from app.config import constants
from app.utility import common
from app.models import items
from app.oauth2 import verify_access_token, verify_bucket_access
from app.utils import generate_download_signed_url_v4


router = APIRouter()
@router.get("/item/health-check")
def health_check(request: Request):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        dict_resp["status"] = True
        dict_resp["msg"] = "healthy"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.get("/item/list/{bucket_id}/{sub_bucket_id}/{page}/{count_per_page}")
def list_item(request: Request, bucket_id: str, sub_bucket_id: int, page: int = 1, count_per_page: int = 10):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if verify_bucket_access(jwt_token, bucket_id):
            dict_resp["status"] = True
            dict_resp["msg"] = "Fetched successfully"
            bucket_name = items.get_bucket_name(bucket_id)
            if bucket_name:
                list_items = items.list_item(bucket_id, sub_bucket_id, page, count_per_page)
                for item in list_items:
                    item["signed_url"] = generate_download_signed_url_v4(bucket_name, item["name"])
                dict_resp['data'] = list_items
            else:
                dict_resp["msg"] = "Invalid bucket"
        else:
            dict_resp["msg"] = "Bucket access unauthorized"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.get("/item/get/{bucket_id}/{sub_bucket_id}/{itemid}")
def list_item(request: Request, bucket_id: str, sub_bucket_id: int, itemid: str):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if verify_bucket_access(jwt_token, bucket_id):
            dict_resp["status"] = True
            dict_resp["msg"] = "Fetched successfully"
            bucket_name = items.get_bucket_name(bucket_id)
            if bucket_name:
                list_items = items.get_item(bucket_id, sub_bucket_id, itemid)
                item = {}
                if len(list_items) > 0:
                    item = list_items[0]
                    item["signed_url"] = generate_download_signed_url_v4(bucket_name, item["name"])
                dict_resp['data'] = item
            else:
                dict_resp["msg"] = "Invalid bucket"
        else:
            dict_resp["msg"] = "Bucket access unauthorized"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.post("/item/tag/{bucket_id}/{sub_bucket_id}")
def tag_item(request: Request, bucket_id: str, sub_bucket_id: int, req_item: dict):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if verify_bucket_access(jwt_token, bucket_id):
            dict_item = req_item.copy()
            if common.validate_dict(dict_item, ["id", "flag"]):
                if dict_item["flag"] in [1,2]:
                    bucket_name = items.get_bucket_name(bucket_id)
                    if bucket_name:
                        list_items = items.get_item(bucket_id, sub_bucket_id, dict_item["id"])
                        if len(list_items) > 0:
                            item = list_items[0]
                            if item["flag"] == 0:
                                item["flag"] = dict_item["flag"]
                                items.move_item(bucket_id, sub_bucket_id, item["name"], item["flag"])
                                upd_item = items.update_item(bucket_id, sub_bucket_id, dict_item["id"], item)
                                upd_item["signed_url"] = generate_download_signed_url_v4(bucket_name, upd_item["name"])
                                dict_resp["msg"] = "Tagged successfully"
                                dict_resp['data'] = upd_item
                            else:
                                dict_resp["msg"] = "item is already tagged"
                        else:
                            dict_resp["msg"] = "invalid item id"
                    else:
                        dict_resp["msg"] = "invalid bucket"
                else:
                    dict_resp["msg"] = "Invalid flag"
            else:
                dict_resp["msg"] = "id and flag must not be empty"
        else:
            dict_resp["msg"] = "Bucket access unauthorized"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

@router.get("/item/sync/{bucket_id}/{sub_bucket_id}")
def sync_bucket(request: Request, bucket_id: str, sub_bucket_id: int, limit: int = 10, page_token: str = None):
    dict_resp = constants.default_response.copy()
    jwt_token = common.get_token(request, "jwt")
    if verify_access_token(jwt_token):
        if verify_bucket_access(jwt_token, bucket_id):
            dict_resp["status"] = True
            dict_resp["msg"] = "Access authorized"
            list_items = []
            bucket_name = items.get_bucket_name(bucket_id)
            if bucket_name:
                page_token = items.get_item_by_page(list_items, bucket_id, limit, page_token, sub_bucket_id)
                while page_token:
                    page_token = items.get_item_by_page(list_items, bucket_id, limit, page_token, sub_bucket_id)
                dict_resp["items"] = list_items
                dict_resp["items_count"] = len(list_items)
            else:
                dict_resp["msg"] = "invalid bucket"
        else:
            dict_resp["msg"] = "Bucket access unauthorized"
    else:
        dict_resp["msg"] = "Access unauthorized"
    return dict_resp

# 