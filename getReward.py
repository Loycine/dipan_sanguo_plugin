#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
from utils import *
import typing


url = get_url('OPT', 63)

default_city_cid = 12408
default_city_gid = 596490
headers = get_headers(default_city_cid, default_city_gid)

r = requests.post(url, headers=headers, timeout=10)
print(r.text)