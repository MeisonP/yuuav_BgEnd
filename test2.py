import requests
import unit
import json
import logging

project_id=154
coordinate={'sW_lat': 30.862550831631065, 'nE_lon': 121.9122533888862, 'sW_lon': 121.90872000695002, 'nE_lat': 30.865288715937975}
def get_Locus(project_id, **coordinate):
    url_get_Locus_bboxs = "http://atilas.locussocial.com/diff/timetag/"
    print url_get_Locus_bboxs
    payload = "{\n  \"time\": %d,\n          \n  \"scope\":{\n    \"latSw\": %f,\n    \"lngSw\":  %f,\n    \"latNe\":  %f,\n    \"lngNe\":  %f\n  }\n}" \
              % (project_id, coordinate['sW_lat'], coordinate['sW_lon'], coordinate['nE_lat'], coordinate['nE_lon'])
    print payload
    headers_tmp = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "50894378-8e61-4cdf-ad8b-473062b0a4d9"
    }
    print  headers_tmp
    logging.info('requests.....')
    response = requests.request("POST", url_get_Locus_bboxs, data=payload, headers=headers_tmp)
    logging.info('requests done, get response....')
    dict_ = json.loads(response.text)

    return dict_
dict_=get_Locus(project_id, **coordinate)
print dict_