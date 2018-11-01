import requests
import json
import pymysql
import logging
import time
import sys
sys.path.append('../../yuuav_background_mason')
import unit

def image_(project, task):#get info of task processed that upload to locus
    url_task = "http://atilas.locussocial.com:9876/api/projects/{}/tasks/{}".format(project,task)

    response_task = requests.request("GET", url_task, headers=unit.headers_())
    dict_ = json.loads(response_task.text)
    image_count = dict_['images_count']

    return image_count

def main(project, task, date_time):
    # after task processed in locus, obtain tile's lat&lon and transfer to google xy,
    #  and save google_xy and project task id to database table GOOGLEXY2ID
    TM,TM_=unit.int_('get_xy2db')

    bounds_,coordinate = unit.get_bounds(project, task)
    #coordinate is a dict, and bounds is a list respectivelly.

    google_xyz = unit.cvtLatlon2xyz(18, *bounds_)

    image_count=image_(project,task)
    #########to talbe GOOGLEXY2ID
    unit.to_table_GOOGLEXY2ID(project, task, date_time, image_count, bounds_,google_xyz)





