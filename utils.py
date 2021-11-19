#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import cv2 as cv
import numpy as np

from PIL import Image

cities = {"ret":0,"infos":[[4,12407,"有凤来仪",1398897,-105,-409,0,3],[2,-1653,"潇湘玉的营寨",1397584,-105,-408,12407,1],[2,-1654,"石矿",1397585,-104,-408,12407,1],[2,-1655,"铁矿",1397586,-103,-408,12407,1],[2,-1656,"粮食",1397587,-102,-408,12407,1],[2,-1657,"木材",1410713,-106,-418,12407,1],[1,12408,"怡红快绿",596490,-269,202,0,3],[2,-1658,"祁山九寨",595177,-269,203,12408,1],[1,12409,"蘅芷清芬",1493232,-306,-481,0,3],[1,12410,"凉州",444999,548,318,0,3],[2,-1659,"凉州石矿",443686,548,319,12410,1],[2,-1660,"凉州木材",443687,549,319,12410,1],[2,-1661,"凉州铁矿",443688,550,319,12410,1],[2,-1662,"凉州粮食",443689,551,319,12410,1],[1,12411,"幽州",941558,-520,-61,0,3],[3,12412,"幽州平冈",112546,284,571,0,3],[3,12413,"西凉二郡",1117158,451,-194,0,3],[1,12414,"西凉一郡",1237124,-379,-286,0,3],[1,12415,"南郡",511035,-379,267,0,3],[1,12416,"潇湘玉的新城",680889,98,138,0,3],[3,12417,"潇湘仙仙的新城",404617,-444,348,0,3],[1,18559,"怡红快绿陪都",599115,-270,200,0,1],[1,18560,"幽州陪都",945497,-520,-64,0,1]]}


city_names = {}
for city in cities['infos']:
    city_names[city[1]] = city[2]
city_gids = {}
for city in cities['infos']:
    city_gids[city[1]] = city[3]
    
resource_names = {1:"food", 2:"wood", 3:"stone", 4:"iron"}


import random
import requests
def get_url(type, id):
    return f'http://sg52.dipan.com/GateWay/{type}.ashx?id={id}&{random.random()}'


def get_headers(cid, mid):
    cookie = f"your_cookie"
    headers = {
    'Host': 'sg52.dipan.com',
    'Connection': 'keep-alive',
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'X-Prototype-Version': '1.5.0',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://sg52.dipan.com',
    'Referer': 'http://sg52.dipan.com/city',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7',
    'Cookie': f'{cookie}',
    }
    return headers


def get_verify_headers():
    cookie = "your_cookie"
    headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'sgmap-cdn.dipan.com',
    'Referer': 'http://sg52.dipan.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Cookie': f'{cookie}',
    }
    return headers


def my_read_img(file_name):
    gif = cv.VideoCapture(file_name)
    ret,frame = gif.read() # ret=True if it finds a frame else False. Since your gif contains only one frame, the next read() will give you ret=False
    return frame

def get_the_ans(numbers):
    # input numbers = [136, 230, 415, 457]
    ans = []
    for number in numbers:
        img1 = my_read_img(f"imgs/{number}.gif")
        img2 = my_read_img("imgs/verifyCode.gif")

        MIN_MATCH_COUNT = 10
        # Initiate SIFT detector
        sift = cv.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)

        ans.append((number,len(good)))
    ans.sort(key=lambda x:x[1])
    # return ans = [(415, 1), (457, 9), (230, 18), (136, 22)]
    return ans


import logging
def init_local_logger(logFilename, loggerName):
    logging.basicConfig(
                    level    = logging.INFO,
                    format   = '%(message)s',
                    # format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt  = '%Y-%m-%d %H:%M',
                    filename = logFilename,
                    filemode = 'a+')
  
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s', datefmt='%Y-%m-%d %H:%M')
    console.setFormatter(formatter)
    logging.getLogger(loggerName).addHandler(console)
    return logging.getLogger(loggerName)