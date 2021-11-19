#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import random
from utils import *
import json


def increase_morale_for_all_cities():
    """if morale down > 0, then increase morale in the city"""
    url = f'http://sg52.dipan.com/GateWay/OPT.ashx?id=4&{random.random()}'
    cnt = 0
    for city in cities["infos"]:
        if city[0] != 2:
            info_url = get_url('City', 6)
            headers = get_headers(city[1], city[3])
            try:
                r = requests.post(info_url, headers=headers, timeout=10)
                morale_down = r.json().get('morale')[2]
                if morale_down > 0:
                    form_data = {'lType': '3', 'tid': '0'}
                    r = requests.post(url, headers=headers, timeout=10, data=form_data)
                    logger.info(f'{city_names[city[1]]} government check morale down: {morale_down}, retCode: {r.text}')
                    cnt = cnt + 1
            except (requests.exceptions.RequestException, requests.exceptions.RequestException,json.JSONDecodeError):
                logger.info("Timeout")


def increase_people_for_all_cities():
    url = f'http://sg52.dipan.com/GateWay/OPT.ashx?id=4&{random.random()}'
    cnt = 0
    for city in cities["infos"]:
        if city[0] != 2:
            headers = get_headers(city[1], city[3])
            form_data = {'lType': '4', 'tid': '0'}
            try:
                r = requests.post(url, headers=headers, timeout=10, data=form_data)
                logger.info(r.text)
                cnt = cnt + 1
            except (requests.exceptions.RequestException, requests.exceptions.RequestException,json.JSONDecodeError):
                logger.info("Timeout")


if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    logger.info("Government")
    logger.info('------------------------------------------------------')
    increase_morale_for_all_cities()
    logger.info('------------------------------------------------------')
