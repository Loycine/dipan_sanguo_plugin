#!/usr/bin/python
# -*- coding: UTF-8 -*-

from types import resolve_bases
import requests
import json
import random

from requests.models import Response
from utils import *
import typing

default_city_cid = 12408
default_city_gid = 596490
headers = get_headers(default_city_cid, default_city_gid)

def researchTech(techid):
    default_city_cid = 12408
    default_city_gid = 596490
    headers = get_headers(default_city_cid, default_city_gid)
    url = get_url('City', 37)
    form_data={
        'ttid': 0,
    }
    r = requests.post(url, headers=headers, timeout=10, data=form_data)
    print(r.text)
    current_tech = json.loads(r.text).get('tech')[0] 

    if current_tech == 0:
        url = get_url('OPT', 44)
        form_data = {
            'techid': techid,
            'tid': 0,
        }
        
        r = requests.post(url, headers=headers, timeout=10, data=form_data)
        logger.info(f"Technology: target_tech: {techid}, retCode: {r.text}")
        return 0
    else:
        logger.info(f"Technology: current_tech: {current_tech}")
        return -1

tech_ids = [7, 4,  8, 9, 19, 27,  29, 1, 2, 3]
if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    logger.info("Technology")
    logger.info('------------------------------------------------------')
    for id in tech_ids:
        ret = researchTech(7)
        if ret == -1:
            break
    logger.info('------------------------------------------------------')