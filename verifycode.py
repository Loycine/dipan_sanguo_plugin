#!/usr/bin/python
# -*- coding: UTF-8 -*-

from types import resolve_bases
import requests
import json
import random

from requests.models import Response
from utils import *
import typing
import os

def submit_verify_code():
    default_city_cid = 12407
    default_city_gid = 1398897

    try_url = f'http://sg52.dipan.com/GateWay/OPT.ashx?id=4&{random.random()}'
    headers = get_headers(default_city_cid, default_city_gid)
    form_data = {
        'lType': '4',
        'tid': '0',
    }
    '''
    try_ret =  requests.post(try_url, headers=headers, timeout=10, data=form_data)
    logger.info(try_ret.text)
    if json.loads(try_ret.text).get('ret') == 110:
        logger.info('ok')
    '''


    url = 'http://sg52.dipan.com/VerifyCode.gif?t='+f'{8599}&xf={random.random()}'
    r = requests.get(url, headers=headers, timeout=10)
    with open('imgs/verifyCode.gif', 'wb') as f:
        f.write(r.content)


    import demjson
    ret_url = f'http://sg52.dipan.com/GateWay/Common.ashx?id=73&{random.random()}'
    ret = requests.post(ret_url, headers=headers, timeout=10)
    logger.info(f'response info: {ret.text}')
    image_ids = demjson.decode(ret.text).get("list")
    ids = []
    for x in image_ids:
        ids.append(x[0])

        if os.path.exists(f'imgs/{x[0]}.gif'):
            continue
        image_url = f'http://sgmap-cdn.dipan.com/Statics/Images/history/{x[0]}.gif'
        r = requests.get(image_url, headers=get_verify_headers(), timeout=20)
        with open(f'imgs/{x[0]}.gif', 'wb') as f:
            f.write(r.content)  
    logger.info(f'image ids: {ids}')


    ans = get_the_ans(ids)
    logger.info(f'predict ans: {ans}')
    num = ans[0][0]
    url = f'http://sg52.dipan.com/GateWay/OPT.ashx?id=102&{random.random()}'
    headers = get_headers(default_city_cid, default_city_gid)
    form_data = {
        'num' : f'{num}'
    }
    r = requests.post(url, headers=headers, timeout=10, data=form_data)
    logger.info(f'retCode: {r.text}')



if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    logger.info("VerifyCode")
    logger.info('------------------------------------------------------')
    max_epoch_times = 5
    for epoch in range(max_epoch_times):
        try:
            logger.info(f'# Submit verify code: times: {epoch+1}')
            submit_verify_code()
            logger.info(f"VerifyCode Success in times: {epoch+1}")
            break
        except (requests.exceptions.RequestException, requests.exceptions.RequestException,json.JSONDecodeError):
            logger.info("Timeout")
    logger.info('------------------------------------------------------')