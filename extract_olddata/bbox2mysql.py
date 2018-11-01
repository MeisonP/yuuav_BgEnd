# coding:utf-8
# 从Locus 获取识别结果bbox并存储数据库

import requests
import json
import pymysql
import logging
import time
import sys
sys.path.append('../../yuuav_background_mason')
import unit



def read_index_table():
    logging.info('read index table from database to get id_project and task bounds')

    try:
        logging.info('connet to MySQL...')
        db = pymysql.connect(host='localhost', port=3306, user="root", passwd="pengdeng90", db="masondb",
                             charset='utf8')
    except:
        logging.error('connet to MySQL failed!')
        raise

    cursor = db.cursor()
    logging.info('connet to MySQL successed!, beging read date table')

    sql_read="""select PROJECT_ID, TASK_ID,sW_lat,sW_lon,nE_lat,nE_lon from GOOGLEXY2ID"""

    try:
        cursor.execute(sql_read)
    except:
        logging.error('cursor execute error!')
        raise
    result=cursor.fetchall()
    logging.error('fetchall of sql')
    db.close()

    return result



#######################################
if __name__ == '__main__':
    TM,TM_=unit.int_('bbox2mysql')

    coordinate = {}
    table=read_index_table()
    count=1
    for row in table:
        id_project=row[0]
        id_task=row[1]
        coordinate['sW_lat']=row[2]
        coordinate['sW_lon']=row[3]
        coordinate['nE_lat']=row[4]
        coordinate['nE_lon']=row[5]

        bbox_list, box_numbers=unit.get_Locus_bboxs(id_project,**coordinate)

        unit.to_table_BBOXS(id_project, id_task, box_numbers, TM_, *bbox_list)

        count=count+1











