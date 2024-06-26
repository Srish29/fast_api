default_response = {
    'status': False,
    'msg': ''
}

ACCESS_TOKEN_EXPIRE_MINUTES = 30

BUCKETS = {
    'casting' : 'casting_product_image_data',
    'm_and_m' : 'vision_mm',
    'admin' : ['casting_product_image_data', 'vision_mm']   
}

dict_bucket = {
    "cpid_1": {
        "name": "casting_product_image_data",
        "page": {
            1: {
                "is_move": True,
                "flag":{
                    0 : 'casting_data_512_original/unclassified_raw/',
                    1 : 'casting_data_512_original/ok/',
                    2 : 'casting_data_512_original/def/'
                },
            },
            2: {
                "is_move": False,
                "flag":{
                    0 : 'casting_data_512_original/annotated/',
                    1 : 'casting_data_512_original/annotated_ok/',
                    2 : 'casting_data_512_original/annotated_error/'
                }
            },
        },
    },
    "vm_1": {
        "name": "vision_mm",
        "page": {
            1: {
                "is_move": True,
                "flag":{
                    0 : 'casting_data_512_original/unclassified_raw/',
                    1 : 'casting_data_512_original/ok/',
                    2 : 'casting_data_512_original/def/'
                },
            },
            2: {
                "is_move": False,
                "flag":{
                    0 : 'casting_data_512_original/annotated/',
                    1 : 'casting_data_512_original/annotated_ok/',
                    2 : 'casting_data_512_original/annotated_error/'
                }
            },
        },
    }
}

TAGS = {
    "RAW" : 0,
    "OK" : 1,
    "DEFECT" : 2
}

