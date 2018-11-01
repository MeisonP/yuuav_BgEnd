#coding:utf-8
#2018-07-11
import requests
import json
import pymysql
import logging
import time
import unit
from flask import Flask,request,send_file
from back2locus import get_bbox2db, get_xy2db


app = Flask(__name__)

@app.route('/back2locus/',methods=['GET'])
def locus_to_mydql():#
    logging.info('flask locus_to_mydql func: anyalizing request parameters...')
    try:
        project_id=request.args.get('project_id')
        task_id=request.args.get('task_id')
        date_time=request.args.get('date_time')
    except:
        logging.error('requested parameters error, please check your request!')
        raise

    logging.info('parameters anylasis doen, check status...')
    status = unit.get_status(project_id, task_id)
    if status == 40:
        #############
        logging.info('image processing done at locus, calling mdoel:get_bbox2db and get_xy2db...')

        try:
            logging.info('model get_bbox2db')
            #get bbox from locus and save to mysql
            get_bbox2db.main(project_id, task_id, date_time)

            logging.info('model get_xy2db')
            #get info save to mysql googlexy2id table
            get_xy2db.main(project_id, task_id, date_time)
        except:
            logging.info('model calling failed!', exec_info=True)
            return 'model calling failed!'
            raise

        msg = 'model get_bbox2db and get_xy2db calling done, and data have been stored into YUUAV database, now back to flask.'
        logging.info('{}'.format(msg))
        return msg
        #####
    else:
        logging.error('processing image....please waite!')


#after the upload images are processed by locus, then save the info to mysql
if __name__ == '__main__':
    TM,TM_=unit.int_('flaskapp_back2locus')
    logging.info('Hello, this is YUUAV flask app, waiting for request ....')

    app.run()

'''
#test
############################
import requests
# text front2back app time2map
url_haha= 'http://localhost:5000/back2locus/'

querystring_haha= {"project_id": "193", "task_id": "2534", "date_time": "20180714"}

response = requests.request('GET', url_haha, params=querystring_haha)
image_src = response.text

print image_src
'''