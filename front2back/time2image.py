#coding:utf-8
#2018-07-11
import requests
import json
import pymysql
import logging
import time
import sys
sys.path.append('../../yuuav_background_mason')
import unit



def select_project_task(from_time,to_time,*google_xyz):
    try:
        logging.info('connet to MySQL...')
        db = unit.get_db()
    except:
        logging.info('connet to MySQL failed!')
        raise

    cursor=db.cursor()

    sql = """select PROJECT_ID, TASK_ID, GOOGLE_X, GOOGLE_Y, GOOGLE_Z from GOOGLEXY2ID 
              where (DATE_TIME between {0} and {1}) 
                    and GOOGLE_X={2[0]} and GOOGLE_Y={2[1]} and GOOGLE_Z={2[2]}""".format(from_time,to_time,google_xyz)

    try:
        cursor.execute(sql)
        db.commit()

    except:
        logging.error("sql_execute commit failed!")
        raise

    results=cursor.fetchall()

    db.close()

    return results



def main(from_time,to_time,*google_xyz):
    TM,TM_=unit.int_('time2image')

    results_list=select_project_task(from_time,to_time,*google_xyz)

    return results_list
