#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
from utils import *


default_city_cid = 12407
default_city_gid = 1398897


def get_all_offical():
    url = get_url("Common", 32)
    headers = get_headers(default_city_cid, default_city_gid)

    form_data = {
        "type" : "1"
    }

    try:
        r = requests.post(url, headers=headers, timeout=10, data=form_data)
        logger.info(r.text)
        return json.loads(r.text).get('list')
    except requests.exceptions.RequestException:
        logger.info("Timeout")
    return []


def add_attribute_for_all_offical():
    officals_all = get_all_offical()
    if len(officals_all) == 0:
        return
    
    officals_in_pending = []
    for city_info in officals_all:
        officals_in_city = city_info[-1]
        for offical in officals_in_city:
            if offical[7] < 100:
                logger.info(offical[7])
                diff = 100 - offical[7]
                level = offical[6]
                money = diff * level * 10

                money = min(money, 300000)
                url = get_url('OPT', '46')
                headers = get_headers(default_city_cid, default_city_gid)
                form_data = {
                    "lCityID": f"{city_info[0]}",
                    "lGeneralID": f"{offical[0]}",
                    "lMoney": f"{money}",
                }
                
                try:
                    r = requests.post(url, headers=headers, timeout=10, data=form_data)
                    logger.info(r.text)
                    ret = json.loads(r.text).get('ret')
                    if ret == 0:
                        logger.info(json.loads(r.text).get('loyalty'))
                except (requests.exceptions.RequestException,json.JSONDecodeError):
                    logger.info("Timeout")

            if offical[-1] > 0:
                officals_in_pending.append([city_info[0], offical[0], offical[-1]])
                

    for offical in officals_in_pending:
        url = get_url("OPT", 67)
        headers = get_headers(default_city_cid, default_city_gid)

        times = offical[-1]//10
        cur_attribute_type = 3
        time = 0
        while time < times:
            form_data = {
                "lCityID" : f"{offical[0]}",
                "lGeneralID" : f"{offical[1]}",
                "lAttribType": f"{cur_attribute_type}",
                "lAdd": "10"
            }

            try:
                r = requests.post(url, headers=headers, timeout=10, data=form_data)
                logger.info(r.text)
                ret = json.loads(r.text).get('ret')
                if ret == 77:
                    cur_attribute_type = 1 if cur_attribute_type == 3 else 3
                    time = time -1
                if ret == 0:
                    cur_attribute_type = 3
                
            except requests.exceptions.RequestException:
                logger.info("Timeout")

            time = time + 1


if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    logger.info("Official")
    logger.info('------------------------------------------------------')
    add_attribute_for_all_offical()
    logger.info('------------------------------------------------------')