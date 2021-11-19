#!/usr/bin/python
# -*- coding: UTF-8 -*-

from types import resolve_bases
import requests
import json
import random

from requests.models import Response
from utils import *
import typing


jobs = [[12408,city_gids[12408], 18559, 330000], [12415, city_gids[12415], 12417, 290000], [12411, city_gids[12411], 18560,330000]]
url = get_url('OPT', 52)
    
def auto_send_res_for_all_jobs():
    for job in jobs:
        try:
            headers = get_headers(job[0],job[1])
            form_data = {
                'tid': '0',
                'gid': '0',
                'gamount': '0',
                'Wood': '0',
                'Iron': '0',
                'Stone': '0',
                'Food': '0',
                'Money': f'{job[3]}',
                'times': '1',
                'dest': f'{job[2]}',
            }
            r = requests.post(url, headers=headers, timeout=10, data=form_data)
            logger.info(f'Send {job[3]} Money: From {city_names[job[0]]} to {city_names[job[2]]}, retCode: {r.text}')
        except (requests.exceptions.RequestException, requests.exceptions.RequestException,json.JSONDecodeError):
            logger.info("Timeout")


army_jobs = [[12412, city_gids[12412]]]
def auto_morale():
    try:
        for job in army_jobs:
            url = get_url('OPT', 47)
            headers = get_headers(job[0],job[1])
            form_data = {
                'lAddPoint': '10',
                'lGeneralID': '64456',
                'tid': '0',
            }

            r = requests.post(url, headers=headers, timeout=10, data=form_data)
            logger.info(f'Train army: In {city_names[job[0]]}, retCode: {r.text}')
    except (requests.exceptions.RequestException, requests.exceptions.RequestException,json.JSONDecodeError):
        logger.info("Timeout")


if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    logger.info("SendRes")
    logger.info('------------------------------------------------------')
    auto_send_res_for_all_jobs()
    auto_morale()
    logger.info('------------------------------------------------------')

