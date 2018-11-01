#coding:utf-8
#2018-07-11
import requests
import json
import pymysql
import logging
import time
import unit
from flask import Flask,request,send_file
import sys
sys.path.append('./')
from front2back import time2bbox,time2image

app = Flask(__name__)

# return json bbox list  for bbox func
# and return image file for google_xyz func ,get image from locus using project_id ,task_id and google_xyz
def download_image(list): #list include project task google_xyz
    url_download_image= "http://atilas.locussocial.com/tiles"
    for row in list:
        id_project=row[0]
        id_task=row[1]
        google_X=row[2]
        google_Y=row[3]
        google_Z=row[4]

        querystring = {"z":google_Z,"x":google_X,"y":google_Y,"timetag":id_project}
        headers = unit.headers_()
        response_image= requests.request("GET", url_download_image, headers=headers, params=querystring)
        image_src=response_image.content


        #return image_src

        name='x={}_y={}_z={}_timetag={}.png'.format(querystring['x'],querystring['y'],querystring['z'],querystring['timetag'])
        with open('./src/{}'.format(name),'a')as f:
            f.write(image_src)
            f.close()
        return name


#front-end should pass: google_xyz,and time to get image_src
@app.route('/front2back/time2map',methods=['GET'])
def get_image():# front-end request tile png in time , at x,y,z
    logging.info('flask get_image func: anyalizing request parameters...')
    try:
        from_time=request.args.get('from_time')
        to_time=request.args.get('to_time')
        google_x=request.args.get('google_x')
        google_y = request.args.get('google_y')
        google_z = request.args.get('google_z')
        google_xyz=[google_x,google_y,google_z]
    except:
        logging.error('requested parameters error, please check your request!')
        raise

    logging.info('parameters anylasis doen, calling convert_mdoel:time2image...')
    try:
        # list include project task google_xyz that meetting the request
        prject_task_list=time2image.main(from_time,to_time,*google_xyz)
    except:
        logging.error('model calling failed!')
        raise
    logging.info('convert done, back to flask.')
    try:
        logging.info('begin to download image source form locus')
        #download the image source that meeting request from locus
        name=download_image(prject_task_list)
    except:
        logging.error('download image source from locus failed!')
        raise

    # pass the image_src to front-end , and front-end should write this src into png file
    logging.info('image source prepared, return to client...')

    return send_file('./src/{}'.format(name),mimetype="image/png")



#front-end should pass:viewport bounds and time to get bbox
@app.route('/front2back/time2detect', methods=['GET'])
def get_bbox():#front-end request detect results in time
    logging.info('flask get_bbox func: anyalizing request parameters...')
    try:
        label=request.args.get('label')
        from_time=request.args.get('from_time')
        to_time=request.args.get('to_time')
        sW_lat=request.args.get('sW_lat')
        sW_lon=request.args.get('sW_lon')
        nE_lat = request.args.get('nE_lat')
        nE_lon = request.args.get('nE_lon')
    except:
        logging.error('requested parameters error, please check your request!')
        raise

    viewport=[sW_lat,sW_lon,nE_lat,nE_lon]

    logging.info('parameters anylasis doen, calling mdoel:time2bbox...')
    try:
        list_bbox=time2bbox.main(label,from_time,to_time,*viewport) # model of search bbox in time

    except:
        logging.error('model calling failed!')
        raise

    logging.info('convert done, back to flask.')
    js = json.dumps(list_bbox)


    return js

if __name__=="__main__":
    TM,TM_=unit.int_('flaskapp_front2back')
    print TM
    app.run()



'''
#coding:utf-8
import requests
import json
import pymysql
import logging
import time
import sys
import cv2
#sys.path.append('../../yuuav_background_mason')
import unit
from flask import Flask,request

app = Flask(__name__)
############################
#text front2back app time2map
url='http://localhost:5000/front2back/time2map'

querystring = {"from_time":"20180712","to_time":"20180712","google_x":"219834","google_y":"107396","google_z":"18"}

response=requests.request('GET',url,params=querystring)
image_src=response.content


name='x={}_y={}_z={}.png'.format(querystring['google_x'],querystring['google_y'],querystring['google_z'])
with open('{}'.format(name),'a') as f:
    f.write(image_src)
    f.close()
    
############################
#test fron2back app time2bbox

#text front2back app
url='http://localhost:5000/front2back/time2detect'

querystring={"label":"building","from_time":"20180710","to_time":"20180710","sW_lat":"30.862550831631065","sW_lon":"121.90872000695002","nE_lat":"30.865288715937975","nE_lon":"121.9122533888862"}
#querystring = {"from_time":"20180712","to_time":"20180712","google_x":"219834","google_y":"107396","google_z":"18"}

response=requests.request('GET',url,params=querystring)
bbox=response.text
print image_src
js_=json.dumps(bbox)
print js_
'''