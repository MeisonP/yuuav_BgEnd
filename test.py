
# coding:utf-8
import requests
import json
import pymysql
import logging
import time
import sys
import cv2
# sys.path.append('../../yuuav_background_mason')
import unit
url='http://localhost:5000/front2back/time2detect'

querystring={"label":"building","from_time":"20180710","to_time":"20180710","sW_lat":"30.862550831631065","sW_lon":"121.90872000695002","nE_lat":"30.865288715937975","nE_lon":"121.9122533888862"}
#querystring = {"from_time":"20180712","to_time":"20180712","google_x":"219834","google_y":"107396","google_z":"18"}

response=requests.request('GET',url,params=querystring)
bbox=response.text
print image_src
js_=json.dumps(bbox)
print js_
