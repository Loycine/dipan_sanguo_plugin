#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
from utils import *
import typing

class Wall:
    """Wall Make Army Equip Manager"""
    def __init__(self, count:int=800, max_total:int=7200):
        """
        Create a wall equipment manager
        count: per time 
        """  
        self.count = count
        self.max_total = max_total

    def Wall_MakeArmyEquip_form_data(self, gid):
        form_data = {
            'pos':'0',
            'gid':f'{gid}',
            'count':f'{self.count}',
            'tid':'0',
            'lFaster':'1',
            '_':'',
        }
        return form_data

    def build_Wall_MakeArmyEquip(self, cid:int, gid:int):
        headers = get_headers(cid, gid)
        total = 0
        
        for epoch in range(1, 100):
            # 5 equiments gid ~ (901, 905)
            for gid in range(901, 906):
                url = get_url('OPT', '38')
                form_data = self.Wall_MakeArmyEquip_form_data(gid)
                try:
                    r = requests.post(url, headers=headers, timeout=10, data=form_data)
                    logger.info(r.text)

                    num = json.loads(r.text).get('ret')
                    if num != 0:
                        logger.info("Early Stop, The Wall is Full")
                        return
                    total = total + self.count
                except requests.exceptions.RequestException:
                    logger.info("Timeout")
            if total > self.max_total:
                break

    def build_Wall_MakeArmyEquip_for_all_cities(self):
        for city in cities["infos"]:
            if city[0] != 2:
                cid, gid = city[1], city[3]
                self.build_Wall_MakeArmyEquip(cid, gid)

    def run(self):
        self.build_Wall_MakeArmyEquip_for_all_cities()


def calc_building_priority(elem):
    # warehourse
    if elem[1] == 4:
        return -10000
    # government office
    elif elem[1] == 1:
        return -1000
    # wall
    elif elem[1] == 2:
        return -999
    # market
    elif elem[1] == 11:
        return -998
    # civilian houses, low levels first
    elif elem[1] == 3:
        return -100 + elem[3]
    # Academy
    elif elem[1] == 6:
        return -500
    else:
        return elem[1]

class City():
    """City Buildings Manager"""
    def __init__(self, city_cid:int , city_gid:int) -> None:
        """Create a city buildings manager"""  
        self.city_cid = city_cid
        self.city_gid = city_gid

    def get_city_buildings_infos(self) -> typing.Tuple[list, int]:
        """get all the buildings info in the city"""  
        url = get_url('City', '5')
        headers = get_headers(self.city_cid, self.city_gid)

        try:
            r = requests.post(url, headers=headers, timeout=10)
            resp = json.loads(r.text)
            if resp['ret'] == 0:
                return resp["infos"], resp["size"]
            else:
                return [], 0
        except requests.exceptions.RequestException:
            logger.info("Timeout")
        return [], 0
    

    def update_building(self, form_data: dict) -> int:
        """Update a building, with data defined in the form_data"""  
        url = get_url('OPT', '65')
        headers = get_headers(self.city_cid, self.city_gid)

        try:
            r = requests.post(url, headers=headers, timeout=10, data=form_data)
            logger.info(f'Build pid: {form_data["pid"]}, gid: {form_data["gid"]}, retCode: {r.text}')
            return json.loads(r.text).get('ret')
        except requests.exceptions.RequestException:
            logger.info("Timeout")
        return -1


    def run(self):
        """Plan to upgrade all buildings in order"""
        def get_form_data(pid: int, gid:int)->typing.Dict[str, str]:
            """
            type 1: upgrade
            type 2: downgrade
            """
            form_data = {
            'pid': f'{pid}',
            'gid': f'{gid}',
            'type': '1',
            'tid': f'{self.city_cid}',
            }
            return form_data

        buildings,city_size = self.get_city_buildings_infos()
        if city_size == 0:
            return

        # sort the building by your priority
        buildings.sort(key=lambda elem:elem[1])
        top_level = max(buildings[0][3],buildings[1][3])
        buildings.sort(key=calc_building_priority)
        logger.info(buildings)

        # calc previous work list len
        idarray = []
        for i in range(0, len(buildings)):
            if buildings[i][4] == 1 or buildings[i][4] == 2:
                idarray.append([buildings[i][0], buildings[i][1], buildings[i][5], buildings[i][4]])

        logger.info(f'Previous work list size: {len(idarray)}')
        pre_work_list_len = len(idarray)

        # define the max level corresponding to city size 
        level_up = [0, 10, 20, 33]

        cur_len = 0
        for building in buildings:
            building_pid = building[0]
            building_gid = building[1]
            building_level = building[3]
            building_status = building[4]

            # if building list is full, then stop
            if cur_len + pre_work_list_len >= 3:
                break

            # if it is leveling up or leveling down, then find next building
            if building_status != 0:
                continue
            
            # if it is a military camp, gid ~ (17, 21), then go ahead
            if building_gid >=17 and building_gid <= 21:
                ret = self.update_building(get_form_data(building_pid, building_gid))
                if ret == 0:
                    cur_len = cur_len + 1
                    continue
            # else it should be a city
            # if it is a warehouse, gid = 4, level 30 is enough
            if building_gid == 4 and building_level == 30:
                continue

            # if it is a government office, upgrade when the city_size is enough
            if (building_gid==1 or building_gid==18)and building_level < level_up[city_size]:
                ret = self.update_building(get_form_data(building_pid, building_gid))
                if ret == 0:
                    cur_len = cur_len + 1
                    continue

            # else if it is other buidling,  upgrade when the city_size is enough
            if building_level < level_up[city_size]:
                ret = self.update_building(get_form_data(building_pid, building_gid))
                if ret == 0:
                    cur_len = cur_len + 1
                    continue


if __name__ == "__main__":
    logger = init_local_logger('./log', __name__)
    logger.setLevel(logging.INFO)
    logger.info("AutoCityBuilder")
    logger.info('------------------------------------------------------')
    
    for city in reversed(cities["infos"]):
        if city[0] != -1:
            cid, gid = city[1], city[3]
            logger.info(f'# City: {city_names[cid]}')
            city_manager  = City(cid, gid)
            city_manager.run()

    wall_manager = Wall(100,7200)
    wall_manager.run()
    logger.info('------------------------------------------------------')