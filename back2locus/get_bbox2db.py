#coding:utf-8
#get and save bbox to mysql database

import requests
import json
import pymysql
import logging
import time
import sys
sys.path.append('../../yuuav_background_mason')
import unit


def main(project,task,date_time):
    TM,TM_=unit.int_('get_bbox2db')
    logging.info('time is {}'.format(TM))

    bounds_,coordinate = unit.get_bounds(project, task)
    #coordinate is a dict, and bounds is a list respectivelly.

    google_xyz = unit.cvtLatlon2xyz(18, *bounds_)

    bbox_list, box_numbers=unit.get_Locus_bboxs(project,**coordinate)

    unit.to_table_BBOXS(project, task, box_numbers, date_time, *bbox_list)




