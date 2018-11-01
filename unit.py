#coding:utf-8
import requests
import json
import pymysql
import logging
import time
from pygeotile.tile import Tile

##############################
def get_db():
    db = pymysql.connect(host='localhost', port=3306, user="root", passwd="pengdeng90", db="masondb",charset='utf8')
    return db


##############################
def headers_():
    headers_in= {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Authorization': "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IiIsInVzZXJuYW1lIjoieWFveXVkZXYiLCJ1c2VyX2lkIjo3LCJleHAiOjIxMTk3NDIzNzN9.P5lZolGoEn50GQvti_lgTytUW2TrchoU1Isnwy7Yym8"
    }
    return headers_in



##############################
def getUid():
    code= str(uuid.uuid1())#基于时间戳生成通用唯一标识符
    abc = code.split('-')
    delimiter = ''#1以分隔符为准，划分成了list
    uid_code= delimiter.join(abc)  #等于去除了uid的分隔符
    return uid_code



##############################
def int_(name):
    TM = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    TM_ = time.strftime("%Y%m%d", time.localtime())
    #nfilename='./log/log_{0}_{1}.txt'.format(name,TM),
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s-%(levelname)s: %(message)s")  # filemane='get_bboxs.log',
    logging.info('\n*********************%s Mason_%s*********************' %(TM,name))

    return TM,TM_




###############################
# the js fronte-end only give the lat&lon, background need to tf a
def cvtLatlon2xyz(z,*bounds_):
    logging.info('calculating xyz...')
    cross_lat = (bounds_[0] + bounds_[2]) / 2
    cross_lon = (bounds_[1] + bounds_[3]) / 2
    t = Tile.for_latitude_longitude(longitude=cross_lon, latitude=cross_lat, zoom=z)
    x, y = t.google
    google_xyz = [x, y, z]
    #print x, y
    return google_xyz





##############################
def get_status(project_id, task_id):
    logging.info('get the status from Locus')
    url_get_status= "http://atilas.locussocial.com:9876/api/projects/{}/tasks/{}".format(project_id, task_id)
    headers = headers_()
    response = requests.request("GET", url_get_status, headers=headers)

    dict_ = json.loads(response.text)

    try:
        status = dict_["status"]
        # uuid=dict_['uuid']

    except:
        logging.error('The project_id or task_id is not exist！')
        raise

    return status






#############################
def get_bounds(project,task):
    logging.info('project:{},task:{},get bounds coordinate info from locus'.format(project,task))
    url_get_bounds= "http://atilas.locussocial.com:9876/api/projects/{}/tasks/{}/orthophoto/tiles.json".format(project,task)
    headers = headers_()
    try:
        response_get= requests.request("GET", url_get_bounds, headers=headers)
    except:
        logging.error('locus requests error!')
        raise

    logging.info('locus response json2dict')
    dict_=json.loads(response_get.text)

    bounds = [
        dict_['bounds'][1],
        dict_['bounds'][0],
        dict_['bounds'][3],
        dict_['bounds'][2]]
    coordinate = {}
    coordinate['sW_lat'] = bounds[0]
    coordinate['sW_lon'] = bounds[1]
    coordinate['nE_lat'] = bounds[2]
    coordinate['nE_lon'] = bounds[3]

    logging.info('return coordinate.')
    return bounds,coordinate






##############################
def get_Locus_bboxs(project_id, **coordinate):
    logging.info('get bboxs list from locussocial:')

    url_get_Locus_bboxs = "http://atilas.locussocial.com/diff/timetag/"
    payload_tmp= "{\n  \"time\": %s,\n          \n  \"scope\":{\n    \"latSw\": %f,\n    \"lngSw\":  %f,\n    \"latNe\":  %f,\n    \"lngNe\":  %f\n  }\n}" \
              % (project_id, coordinate['sW_lat'], coordinate['sW_lon'], coordinate['nE_lat'], coordinate['nE_lon'])
    headers_tmp= {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "50894378-8e61-4cdf-ad8b-473062b0a4d9"
    }
    logging.info('requests.....')
    response = requests.request("POST", url_get_Locus_bboxs, data=payload_tmp,headers=headers_tmp)
    logging.info('requests done, get response....')
    dict_ = json.loads(response.text)
    try:
        bounds = dict_['bounds']  # a list, each list element is a bbox dict{id, label, bbox_list}
        timetag = dict_['timetag']
    except:
        logging.error("response: bboxs INFO Not Found!")
        raise

    bbox_list = bounds
    box_numbers = len(bbox_list)
    logging.info('There are totally %d boxs' % box_numbers)

    return bbox_list, box_numbers





##############################
def to_table_BBOXS(id_project,id_task,box_numbers, date_time, *bboxs_list):
    logging.info('save the bboxs info into database:')

    try:
        logging.info('connet to MySQL...')
        db = get_db()
    except:
        logging.error('connet to MySQL failed!')
        raise

    cursor = db.cursor()


    logging.info('connet to MySQL successed!, beging insert date into mysql table')

    for i in range(0, box_numbers):
        boxs_dict= bboxs_list[i]  # bboxs_list= return's bounds
        timetag = id_project
        box_id=boxs_dict['id']
        box_label= boxs_dict['label']

        #date_time=TM_

        #project_time =photo_time #time.strftime("%Y%m%d%H%M%S", time.localtime())

        points = [boxs_dict['bbox'][0]['lat'], boxs_dict['bbox'][0]['lng'], boxs_dict['bbox'][1]['lat'],
                  boxs_dict['bbox'][1]['lng'],
                  boxs_dict['bbox'][2]['lat'], boxs_dict['bbox'][2]['lng'], boxs_dict['bbox'][3]['lat'],
                  boxs_dict['bbox'][3]['lng']]

        sql_insert= """INSERT INTO BBOXS (PROJECT_ID, BOX_ID, LABEL, P1_LAT, P1_LNG,P2_LAT,P2_LNG,P3_LAT,P3_LNG,P4_LAT,P4_LNG,DATE_TIME,TASK_ID)
                         VALUES ({0},{1},'{2}',{3[0]},{3[1]},{3[2]},{3[3]},{3[4]},{3[5]},{3[6]},{3[7]},{4},{5})"""\
            .format(timetag,box_id,box_label,points,date_time,id_task)

        # sql="""INSERT INTO BBOXS(PROJECT_ID) VALUES ({})""".format(timetag)
        try:

            cursor.execute(sql_insert)

            db.commit()
            #logging.info('The %d row insert commit,project:%d task:%d'%(count,timetag,id_task))
        except:

            db.rollback()
            logging.error('cursor.execute(sql) error，db rollback! ')
            raise
    logging.info('mysql insert successed, close db.')


    db.close()



##############################
def to_table_GOOGLEXY2ID(id_project, id_task, date_time, image_count, bounds_,xyz):
    try:
        logging.info('connet to MySQL...')
        db = get_db()

    except:
        logging.info('connet to MySQL failed!')

    cursor = db.cursor()

    logging.info('write into table GOOGLEXY2ID')
    sql_ = """INSERT INTO GOOGLEXY2ID (PROJECT_ID, TASK_ID, GOOGLE_X, GOOGLE_Y, GOOGLE_Z,DATE_TIME,image_count,sW_lat,sW_lon,nE_lat,nE_lon)
             VALUES ({0},{1},{2[0]},{2[1]},{2[2]},{3},{4},{5[0]},{5[1]},{5[2]},{5[3]})""".format(id_project, id_task, xyz, date_time, image_count, bounds_)
    try:
        cursor.execute(sql_)
        #logging.info('GOOGLEXY2ID commit {}....'.format(row))
        db.commit()
        #row = row + 1

    except:
        # Rollback in case there is any error,
        logging.error('commit error rollback!')
        db.rollback()
        raise
    # close the connetion
    db.close()




##############################