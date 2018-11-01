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



def select_bbox(label_,from_time,to_time,*big_bounds):
    try:
        logging.info('selet bbox connet to MySQL...')
        db = unit.get_db()
    except:
        logging.info('connet to MySQL failed!')
        raise
    cursor=db.cursor()

    sql="""select  PROJECT_ID, TASK_ID, P1_LAT, P1_LNG, P2_LAT, P2_LNG, P3_LAT, P3_LNG, P4_LAT, P4_LNG from BBOXS 
                  where (DATE_TIME between "{0}" and "{1}") and LABEL="{2}" and 
                  ( ((P1_LAT between {3[0]} and {3[2]}) and (P1_LNG between {3[1]} and {3[3]}))
                    or
                    ((P2_LAT between {3[0]} and {3[2]}) and (P2_LNG between {3[1]} and {3[3]}))
                    or 
                    ((P3_LAT between {3[0]} and {3[2]}) and (P3_LNG between {3[1]} and {3[3]}))
                    or 
                    ((P4_LAT between {3[0]} and {3[2]}) and (P4_LNG between {3[1]} and {3[3]})))""".format(from_time,to_time,label_,big_bounds)

    try:
        cursor.execute(sql)
        db.commit()

    except:
        logging.error("sql_execute commit failed!")
        raise
    logging.info('fetchall from database.')
    results=cursor.fetchall()#result is a tuple

    db.close()

    return results



def main(label,from_time,to_time,*big_bounds):
    TM,TM_=unit.int_('time2bbox')

    bbox_list=select_bbox(label,from_time,to_time,*big_bounds)
    #bbox_list=list(bbox_tuple)
    return bbox_list



