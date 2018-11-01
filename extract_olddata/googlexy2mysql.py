# coding:utf-8
# 建立mysql表格将老数据从locus索引出来。

import pymysql
import requests
import json
import logging
import time
from pygeotile.tile import Tile
import sys
sys.path.append('../../yuuav_background_mason')
import unit



def getUid(uuid_):
    code = uuid_
    abc = code.split('-')
    delimiter = ''  #
    uid_code = delimiter.join(abc)
    return uid_code




TM,TM_=unit.int_('xy2mysql')

headers = unit.get_headers()

# search to get old locus data
# get project id list
row = 1  # count for task or mysql row
index = 0  # count for error numbers

for page in range(1, 7):
    logging.info('project page {}'.format(page))

    url_project = "http://atilas.locussocial.com:9876/api/projects/?ordering=-id&page={}".format(page)
    logging.info('requests project ...')

    response_project = requests.request("GET", url_project, headers=headers)
    dict_project = json.loads(response_project.text)
    project_numbers = dict_project['count']
    project_list = dict_project['results']  # [{'id'..'createtime'.},{'id'...'createtime'}]

    for i in project_list:
        id_project = i['id']
        logging.info('project:{}'.format(id_project))

        createtime_project = i['created_at']
        # task_list=i['task'] #can be used that way
        url_task = "http://atilas.locussocial.com:9876/api/projects/{}/tasks".format(id_project)
        logging.info('requests task ...')
        response_task = requests.request("GET", url_task, headers=headers)
        list_task = json.loads(response_task.text)

        for j in list_task:
            id_task = j['id']
            logging.info('page{}, project{}, task{}'.format(page, id_project, id_task))

            uuid = j['uuid']
            uid_code = getUid(uuid)

            status = ['status']
            task_ctime = j['created_at'][0:10]
            image_count = j['images_count']
            available_assets = j["available_assets"]

            if len(available_assets) == 0:

                logging.info(
                    'A orthophoto has not been processed for this task:{}. Tiles are not available'.format(id_task))
                with open('error_task_{}.txt'.format(TM_), 'a') as f:
                    index = index + 1
                    f.write( '\n{}\tproject:{}\ttask:{}\tA orthophoto has not been processed for this task,Tiles are not available'\
                        .format(index, id_project, id_task))

                # continue
            else:
                logging.info('orthophoto available')
                url_tile = 'http://atilas.locussocial.com:9876/api/projects/{0}/tasks/{1}/orthophoto/tiles.json'.format(
                    id_project, id_task)
                logging.info('requests task detial...')
                response_tile = requests.request("GET", url_tile, headers=headers)
                dict_tile = json.loads(response_tile.text)

                try:
                    bounds = dict_tile['bounds']  # two points lat and lon
                except:
                    logging.info('available_assets is not commpleted!')
                    with open('error_task_{}.txt'.format(TM_), 'a') as f:
                        index = index + 1
                        f.write(
                            '\n{}\tproject:{}\ttask:{}\tA orthophoto has not been processed for this task,Tiles are not available'\
                                .format(index, id_project, id_task))
                    continue

                sW_lat = bounds[1]
                sW_lon = bounds[0]
                nE_lat = bounds[3]
                nE_lon = bounds[2]
                bounds_ = [sW_lat, sW_lon, nE_lat, nE_lon]

                google_xyz = unit.cvtLatlon2xyz(18,*bounds_)
                date_time = TM_

                #########to talbe GOOGLEXY2ID
                unit.to_table_GOOGLEXY2ID(id_project, id_task, google_xyz, date_time, image_count, bounds_)




