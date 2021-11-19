#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json

from utils import *
import typing


def get_market_info(resource_type: int, current_city_cid: int, current_city_gid: int) -> typing.List[dict]:
    url = get_url('Common', 38)
    headers = get_headers(current_city_cid, current_city_gid)


    form_data = {
        'stab': '1',
        'type': f'{resource_type}',
        'tid': '0',
    }

    r = requests.post(url, headers=headers, timeout=10, data=form_data)
    return json.loads(r.text).get('infos')


def buy_resource(resource_type: int, count, seqno, seller, buyincount, price, current_city_cid, current_city_gid):
    url = get_url('OPT', 9)
    headers = get_headers(current_city_cid, current_city_gid)

    form_data = {
        'tid': '0',
        'res_hidden': '1',
        'res_jsondata': '{floatid:"res",desc:"木材",value:1,onchange:"Dipan.SanGuo.Build.Market.DropDown2()",data:[{text:"粮食",value:0},{text:"木材",value:1},{text:"石料",value:2},{text:"铁矿",value:3},]}',
        'buyinprice': f'{price}',
        'count': f'{count}',
        'buyincount': f'{buyincount}',
        'seqno': f'{seqno}',
        'seller': f'{seller}',
        'countprice': f'{price}',
        'type3': f'{resource_type}',
    }
    r = requests.post(url, headers=headers, data=form_data, timeout=10)

    logger.info(f'City {city_names[current_city_cid]}: buy resource: {resource_names[resource_type]}, count: {count}, for price: {price}, retCode: {r.text}')



def auto_market_for_one_city(city_cid, city_gid):
    current_city_cid = city_cid
    current_city_gid = city_gid

    url = get_url('City', 20)
    headers = get_headers(current_city_cid, current_city_gid)

    r = requests.post(url, headers=headers, timeout=10)
    resource = json.loads(r.text)

    food = resource['food'][0]
    wood =resource['wood'][0]
    stone = resource['stone'][0]
    iron = resource['iron'][0]
    max_storage = resource['max_storage']

    total = (int)(0.95 * max_storage)
    items = [food, wood, stone, iron]
    for i in range(4):
        resource_type = i + 1
        if items[i] < 0.8 * max_storage:
            diff = total - items[i]
            count = diff // 1000
            market_infos = get_market_info(resource_type, current_city_cid, current_city_gid)

            seqno = market_infos[0]['seqno']
            seller= market_infos[0]['seller']
            buyincount = market_infos[0]['count']
            price = market_infos[0]['price']
            count = min(count, int(buyincount))

            buy_resource(resource_type, count, seqno, seller, buyincount, price, current_city_cid, current_city_gid)


skip_cities = [12417]

def auto_market_for_all_cities():
    for city in cities["infos"]:
        if city[0] != 2:
            city_cid = city[1]
            city_gid = city[3]
            info_url = get_url('City', 6)
            headers = get_headers(city[1], city[3])
            try:
                r = requests.post(info_url, headers=headers, timeout=10)
                current_money = r.json()['money'][0]
            except (requests.exceptions.RequestException, requests.exceptions.RequestException,json.JSONDecodeError):
                current_money = 0
            
            if city_cid in skip_cities or current_money<5000000:
                logger.info(f"{city_names[city_cid]} Skip: for current money: {current_money}")
                continue
            try:
                auto_market_for_one_city(city[1], city_gid)
            except (requests.exceptions.RequestException, requests.exceptions.RequestException,json.JSONDecodeError):
                logger.info("Timeout")


if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    logger.info("AutoMarket")
    logger.info('------------------------------------------------------')
    auto_market_for_all_cities()
    logger.info('------------------------------------------------------')