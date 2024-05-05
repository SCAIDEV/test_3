# from tkinter import E
# from common.utils import CacheHelper, MongoHelper
# from livis.settings import *
# from bson import ObjectId
# import datetime
# import base64
# import uuid 
# import datetime
# from inspection_mobile_app.virtualbutton import *
# from inspection_mobile_app.plcbutton import *
# # from kafka import KafkaProducer,  KafkaConsumer
# import numpy as np
# import sqlite3

# from tkinter import E
from turtle import left, right
from urllib.request import CacheFTPHandler
from common.utils import CacheHelper
from django.http import response
import numpy as np
import cv2 
from numpy import array
import json
import base64
import multiprocessing
import sys
from pymongo import MongoClient
from bson import ObjectId
from livis import settings as settings
from livis.settings import BASE_URL
from livis.settings import *
import os
import time
# import datetime
from datetime import  datetime
from dateutil import tz
import bson


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class MongoHelper:
    from livis.settings import DEV_MACHINE_HOST,DEV_MACHINE_MONGO_PORT
    client = None
    def __init__(self):
        if not self.client:
            self.client = MongoClient(host='localhost', port=27017)
            # self.client = MongoClient(host=DEV_MACHINE_HOST, port=DEV_MACHINE_MONGO_PORT)


        self.db = self.client[settings.MONGO_DB]
        # if settings.DEBUG:
        #     self.db.set_profiling_level(2)
        # placeholder for filter
    """
    def getDatabase(self):
        return self.db
    """

    def getCollection(self, cname, create=False, codec_options=None):
        # _DB = "LIVIS_bluedoor"
        _DB = settings.MONGO_DB
        DB = self.client[_DB]
        return DB[cname]
    
    def createCollection(self ,cname ):
        self.db.create_collection(str(cname))
        return self.db[str(cname)]

####################################################### mobile app +++++++++++++++++++++++++++++++++++++++++++++++++++++


def get_all_parts_mobile_util(data):
    print(data)
    project = data.get("project",None)
    parameter_list = []
    if True: #bool(project ):
        project_mp = MongoHelper().getCollection("parts")
        # print(project_mp)
        col = project_mp.find()
        # col = project_mp.find({"part_number":})
        # print(col)
        for i in col:
            # print(i["part_number"])
            try:
                # if cd project in i["part_number"]:
                parameter = i['part_number']
                part_id = str(i["_id"])
                deployed = check_deployment(part_id)
                if deployed:
                    parameter_list.append(parameter)
            except Exception as e:
                print(e)
        return parameter_list ,200
    return parameter_list , 400





def get_all_regions_util():
    
    # project_mp = MongoHelper().getCollection("regions")
    # col = project_mp.find()
    # regions = []
    # for i in col:
    #     regions.append(i.get('region_name'))
    # return {'regions':regions}, 200
    mp = MongoHelper().getCollection("regions")
    regions =[p for p in  mp.find({'isdeleted' : False})]
    if regions:
        return regions, 200
    else:
        return {},200

   


def check_deployment(part_id):
    print("part_id::::",part_id)
    do_inspection = False
    exp_mp = MongoHelper().getCollection("parts")
    id = ObjectId(part_id)
    col = exp_mp.find({"_id":id})
    # print("col:::",col)
    for i in col:
        # print(i)
        # container_deployed = i["deployed"]
        deployed = i["deployed"]
        # print("container_deployed::::",container_deployed)
        # print("deployed:::",deployed)
        if (deployed == True):
            do_inspection = True
            break
    return do_inspection

def get_class_counts(dc_1,label_list): 
    # print("label_list::",label_list)
    # dict ->  list ->dict
    # All im ->ind  -> ind_prediction
    classes = {}
    #iterate through list of dicts
#     for dc_1 in range(len(label_list)):
    for d2 in label_list[dc_1]:
        # print("d2::",d2)
        label = d2#["label"]
        if label in list(classes.keys()):
            classes[label] += 1
        else:
            classes[label] = 1
    return classes

def get_kanban(parameter_id):
    project_mp = MongoHelper().getCollection("parts")
    col = project_mp.find({"_id":ObjectId(parameter_id)})
    for i in col:
        kanban = i["kanban"]
    return kanban

def check_kanban_1(kanban, predicted_frame_dict_list,label_list,part_id): #usingf
    overall_status = None
    defect_list = []#kanban["defect_list"]
    feature_list = []#kanban["feature_list"]
    kanban_details = {}#kanban["kanban_details"]
    try:
        defect_list = kanban["defects"]
        feature_list = kanban["features"]
        kanban_details = kanban["kanban_details"]
    except Exception as e:
        print(e)
        pass
    resp = {}
    status_list = []
    ind_dict_list = []
    #iterate through predictes frames list and label list
    # print("label_list:::",label_list)
    for dict_key , dc_1 in zip(predicted_frame_dict_list,range(len(label_list))):
        defects = []
        missing_features = []
        predicted_frame = predicted_frame_dict_list[dict_key]
        # print(dict_key,dc_1)
        classes = get_class_counts(dc_1,label_list)
        # print("classes:::",classes)
        #defect 
        for label in list(classes.keys()):
            if label in defect_list:
                defects.append(label)

        #missing parameter
        if len(kanban_details)>0:
            # print("list(kanban_details.keys()):::",list(kanban_details.keys()))
            for kd_label in list(kanban_details.keys()):
                if kd_label in list(classes.keys()):
                    if kanban_details[kd_label] != classes[kd_label]:
                        missing_features.append(kd_label)
                else:
                    missing_features.append(kd_label)
        
        for feature in feature_list:
            if feature in list(classes.keys()):
                pass
            else:
                missing_features.append(feature)
                
        if (len(missing_features) == 0) and (len(defects) == 0):
            status = "accepted"   
        else: 
            status = "rejected"  
        status_list.append(status)

        img_path = f'{IMAGE_STORAGE}/{dc_1}.jpg'
        # print("predicted_frame:::",predicted_frame.shape)
        cv2.imwrite(img_path,predicted_frame)
        # missing_features_dict
        missing_features_dict = {}
        if bool(missing_features):
            # print("missing_features::",missing_features)
            missing_features_classes = np.unique(missing_features)
            for missing_class in missing_features_classes:
                if missing_class in list(kanban_details.keys()):
                    try:
                        missing_features_dict[missing_class] = kanban_details[missing_class] - classes[missing_class]#.count(missing_class)
                    except Exception as e:
                        print(e)
                        missing_features_dict[missing_class] = kanban_details[missing_class] 
                else:
                    missing_features_dict[missing_class] = 1

        # ip_address = BASE_URL #"52.66.203.16" #"server_IP address"
        # url = f"http://{IP_ADDRESS}:8001/gorad/lincode/schneider/Blue_door/standalone/ai_controller/{dc_1}.jpg"
        url = f"http://{IP_ADDRESS}:8001/{dc_1}.jpg"

        ind_dict_list.append({"image_url":url ,"status":status,"missing_features":missing_features_dict,"defects":defects})
        # print("status_list:::",status_list)
    if bool(len(status_list)) :  
        if "rejected"  in status_list:
            overall_status = "rejected"
        else:
            overall_status = "accepted"
        resp = {"overall_status":overall_status,"ind_dict_list":ind_dict_list}
        print(resp)
        return resp 
    return resp

def check_kanban(kanban, predicted_frame_dict_list,prediction_dict_list,part_id): #usingf
    overall_status = None
    overall_defects = []
    overall_missing_features = []
    overall_status_list = []
    defect_list = []#kanban["defect_list"]
    feature_list = []#kanban["feature_list"]
    kanban_details = {}#kanban["kanban_details"]
    ind_dict_list = []
    
    defect_list = kanban["defects"]
    feature_list = kanban["features"]
    try:
        kanban_details = kanban["kanban_details"]
    except Exception as e:
        print(e)
        pass
    resp = {}
    
    print("defect_list::",defect_list)
    print("feature_list::",feature_list)
    print("kanban_details::",kanban_details)
    #iterate through predictes frames list and label list
    for dict_key , dc_1 in zip(predicted_frame_dict_list,range(len(prediction_dict_list))):
        defects = []
        missing_features = []
        missing_features_dict = {}
        
        predicted_frame = predicted_frame_dict_list[dict_key]
        classes = get_class_counts(dc_1,prediction_dict_list)
        #defect 
        for label in list(classes.keys()):
            if label in defect_list:
                defects.append(label)
        #missing parameter
        if len(kanban_details)>0:
            print("kanban_details:::",kanban_details)
            print("list(kanban_details.keys()):::",list(kanban_details.keys()))
            for kd_label in list(kanban_details.keys()):
                if kd_label in list(classes.keys()):
                    if kanban_details[kd_label] != classes[kd_label]:
                        missing_features.append(kd_label)
                        missing_features_dict[kd_label] = kanban_details[kd_label] - classes[kd_label]
                else:
                    missing_features.append(kd_label)
                    missing_features_dict[kd_label] = kanban_details[kd_label] 
        else:
            for feature in feature_list:
                if feature in list(classes.keys()):
                    pass
                else:
                    missing_features.append(feature)
                    missing_features_dict[feature] = 1

        if (len(missing_features) == 0) and (len(defects) == 0):
            status = "accepted"   
        else: 
            status = "rejected"  
        
        # missing_features_dict['dummy'] = "1"

        print("defects:::",defects)
        print("missing_features_dict::::",missing_features_dict)
        print("status::::",status)
        overall_status_list.append(status)
        overall_defects.extend(defects)


        overall_missing_features.extend(missing_features)
        img_path = f'{IMAGE_STORAGE}/{dc_1}.jpg'
        cv2.imwrite(img_path,predicted_frame)
        # url = f"http://{IP_ADDRESS}:8001/gorad/lincode/schneider/Blue_door/standalone/ai_controller/{dc_1}.jpg"
        url = f"http://{IP_ADDRESS}:8001/{dc_1}.jpg"
        # status = "rejected"
        # missing_features_dict['test'] = "1"
        # missing_features_dict = list(missing_features_dict.keys())


        ind_dict_list.append({"image_url":url ,"status":status,"missing_features":missing_features_dict,"defects":defects})
    #Overall status
    if bool(len(overall_status_list)) :  
        if "rejected"  in overall_status_list:
            overall_status = "rejected"
        else:
            overall_status = "accepted"

        # overall_status = "accepted"
        resp = {"overall_status":overall_status,"ind_dict_list":ind_dict_list}
        print(resp)
        return resp 
    return resp


def get_defects_from_mongo():
    mp = MongoHelper().getCollection('parts')
    col = mp.find()
    print(col)
    for i in col:
        kanban = i.get('kanban')
        defects = kanban.get('defects')
    return defects



def get_defect_list(detector_predictions):
	# print(defects)
	defect_list = []
	for i in detector_predictions:
		if i in get_defects_from_mongo():
			defect_list.append(i)
	return defect_list


def check_kanban(defect_list):
    if bool(defect_list):
        is_accepted = "Rejected"
    else:
        is_accepted = "Accepted"
    return is_accepted

def list_to_dict(list_):
    to_dict = {}
    for i in list_:
        if not i in to_dict:
            to_dict[i] = list_.count(i)
    return to_dict



def check_kanban_mongo(inspection_id,predicted_frame_dict_list,prediction_dict_list,parameter,operator_name,mobile_id,part_type):


    overall_status_list = []
    overall_defect_list = []
    ind_dict_list = []

    ind_dict_list_accepted = []
    ind_dict_list_rejected = []
    
    ind_dict_list = []

    ind_dict_list_filter = []


    inference_images = []

    for i,j  in zip(predicted_frame_dict_list,prediction_dict_list):


        region = i
        predicted_frames_dict = predicted_frame_dict_list[i]
        predicted_labels_dict = prediction_dict_list[i]
        print(predicted_labels_dict)

        for dict_key , dc_1 in zip(predicted_frames_dict,predicted_labels_dict):
            print(dict_key,dc_1)
            predicted_frame = predicted_frames_dict[dict_key]
            detector_predictions = predicted_labels_dict[dc_1]

            cv2.imwrite('dummy/'+str(bson.ObjectId())+'.jpg',predicted_frame)


            defect_list = get_defect_list(detector_predictions)
            is_accepted = check_kanban(defect_list)

            overall_status_list.append(is_accepted)
            overall_defect_list.extend(defect_list)
     
            fname = bson.ObjectId()

            cv2.imwrite(datadrive_path+'inspection_images/'+region+'_'+str(fname)+'.jpg',predicted_frame)
            img_url = f"http://{IP_ADDRESS}:8001/inspection_images/{region}_{str(fname)}.jpg"
            inference_images.append(img_url)

            ind_dict_list.append({"image_url":img_url ,"status":is_accepted,"defects":list_to_dict(defect_list),"region":region})
            if is_accepted == 'Rejected':
                ind_dict_list_rejected.append({"image_url":img_url ,"status":is_accepted,"defects":list_to_dict(defect_list),"region":region})
            
            if is_accepted == 'Accepted':
                ind_dict_list_accepted.append({"image_url":img_url ,"status":is_accepted,"defects":list_to_dict(defect_list),"region":region})


            # print(ind_dict_list)


    if bool(len(overall_status_list)) :  
        if "Rejected"  in overall_status_list:
            overall_status = "Rejected"
        else:
            overall_status = "Accepted"

    

    # resp = {"inspection_id":inspection_id, "ind_dict_list":ind_dict_list_filter,"overall_status":overall_status}
    resp = {"inspection_id":inspection_id, "ind_dict_list_accepted":ind_dict_list_accepted,"ind_dict_list_rejected":ind_dict_list_rejected,"overall_status":overall_status}



    inspection_id = inspection_id

    createdAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(createdAt)
    resp_col = resp
    resp_col['createdAt'] = createdAt
    resp_col['created_month'] =  datetime.now().strftime("%m")
    resp_col['created_year'] =  datetime.now().strftime("%Y")
    resp_col['created_date'] =  datetime.now().strftime("%d")

    resp_col['inference_images'] = inference_images
    resp_col['overall_status']=overall_status
    resp_col['overall_defect_list'] = list_to_dict(overall_defect_list)
    resp['part_name'] = parameter
    resp['part_type'] = part_type
    resp['operator_name'] = operator_name
    resp['mobile_id'] = mobile_id
    resp['start_time'] = CacheHelper().get_json('start_time')
    resp['end_time'] = createdAt
    
    resp_col['status'] = 'completed'
    mp = MongoHelper().getCollection(INSPECTION_DATA_LOGS+'_log')
    mp_col = mp.find_one({"$and":[{"status":"started"},{"_id":ObjectId(inspection_id)}]})

    mp.update({'_id' : mp_col['_id']}, {"$set" : resp_col})


    # mp.insert(resp_col)
    
    # resp_col['ind_dict_list'] = ind_dict_list_filter
    return resp_col



def get_inference_mobile_util(data):
#     aircraft_number = data.data.get("aircraft_number",None)
    print(data,'from inference mobile util..')
    t0 = datetime.now()
    CacheHelper().set_json({'start_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    rch = CacheHelper()
    parameter = data.data.get("parameter",None)
    if parameter is None:
        return "Parameter is not present", 400

    mobile_id = data.data.get("mobile_id",None)
    if mobile_id is None:
        return "Mobile ID is not present", 400

    operator_name = data.data.get("operator_name",None)
    if operator_name is None:
        return "Operator Name is not present", 400

    part_type = data.data.get('part_type',None)
    if part_type is None:
        return "Part type is not present", 400
    inspection_id = data.data.get('inspection_id',None)
    if inspection_id is None:
        return "Inspection ID not present", 400

    

    parameter_id = ""
    
    print(parameter,'parameter parameter parameter parameter')
    print(mobile_id,'mobile_id mobile_id mobile_id mobile_id')
    print(operator_name,'operator_name operator_name operator_name operator_name')
    print(part_type,'part_type part_type part_type part_type')


    print(data,'pay load...')
    # mp = MongoHelper().getCollection(INSPECTION_DATA_LOGS+'_log')
    # mp.insert_one({'inspection_status':'started'})
    # print("parameter:::",parameter)

    if bool(parameter):
        #get part id
        project_mp = MongoHelper().getCollection("parts")
        a = project_mp.find({"part_number":parameter})
        print(a,'aaaaaaaaaaaaa')
        for i in a :
            print(i,'iiiiiiiiiiiiiiiiiii')
            parameter_id = i["_id"]
            print(parameter_id,'parameter idddddddddddddddddddddddddddddd')
        # form = NameForm(data.POST)

        #check whether the model in deplyed or not
        deployed_do_inspection = check_deployment(part_id = parameter_id )

        if deployed_do_inspection:
            # print("mobile_id",mobile_id)

            zone_data = {
                        "parameter":parameter_id,
                        "operator_name":operator_name}
            try:
                top_images = data.FILES.getlist('top')
            except:
                    message = "No file provided"
                    status_code = 400
                    return message, status_code
            if not top_images:
                return "Empty file", 200

            try:
                left_images = data.FILES.getlist('left')
            except:
                    message = "No file provided"
                    status_code = 400
                    return message, status_code
            if not left_images:
                return "Empty file", 200

            try:
                right_images = data.FILES.getlist('right')
            except:
                    message = "No file provided"
                    status_code = 400
                    return message, status_code
            if not right_images:
                return "Empty file", 200

            try:
                front_images = data.FILES.getlist('front')
            except:
                    message = "No file provided"
                    status_code = 400
                    return message, status_code
            if not front_images:
                return "Empty file", 200

            try:
                back_images = data.FILES.getlist('back')
            except:
                    message = "No file provided"
                    status_code = 400
                    return message, status_code
            if not back_images:
                return "Empty file", 200
            inspection_files = {'top':top_images,'left':left_images,'right':right_images,'front':front_images,'back':back_images}
            input_image_dict = {}


            for file_region, files in inspection_files.items():
                input_image_array = [] 

                for file in files:
                    img_str = b''
                    for chunk in file.chunks():
                        img_str += chunk
                    nparr = np.fromstring(img_str, np.uint8)
                    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    w,h,c = img_np.shape
                    
                    # img_np = cv2.resize(img_np,(w//2,h//2))#cv2.resize(predicted_frame,(w//2,h//2))
                    # img_np = cv2.resize(img_np,(1280,1080))
                    img_np = cv2.resize(img_np,(640,480))

                    input_image_array.append(img_np)

                    print(img_np.shape)
                
                input_image_dict[file_region] = input_image_array
            
            print(f"size of input_image_dict is :: {sys.getsizeof(input_image_dict)} bytes")
            rch.set_json({f"{mobile_id}_input_image_dict":input_image_dict})
            # rch.set_json({"input_image_dict":input_image_dict})
            # CacheHelper().set_json({'temp':input_image_dict})
            # print(input_image_dict)
            rch.set_json({f"{mobile_id}_parameter":parameter})
            rch.set_json({f"{mobile_id}_mobile_trigger":True})
            print('triggered.....')


            # rch.set_json({f"{mobile_id}_zone_data":zone_data})

            while True:
                inspection_completed = rch.get_json(f"{mobile_id}_inspection_completed")
                mobile_trigger = rch.get_json(f"{mobile_id}_mobile_trigger")
                if mobile_trigger == False:
                    if inspection_completed == True:
                        predicted_frame_dict_list = rch.get_json(f"{mobile_id}_output_frame_list")
                        prediction_dict_list =  rch.get_json(f"{mobile_id}_prediction_dict_list")
                        

                        print(prediction_dict_list,'***************')
                        # temp = predicted_frame_dict_list.get('top')
                        # print(len(temp),'#############################')

                        # inspection_id = str(bson.ObjectId())

                        # inspection_id = INSPECTION_DATA_LOGS
                        # inspection_name = INSPECTION_DATA_LOGS

                        resp = check_kanban_mongo(inspection_id,predicted_frame_dict_list,prediction_dict_list,parameter,operator_name,mobile_id,part_type)
                        rch.set_json({f"{mobile_id}_inspection_completed":False})
                        t1 = datetime.now()

                        print(resp)
                        print(f'Time taken for one complete cycle >>>image transfer and inference GPU:::  {(t1-t0).total_seconds()} sec')
                        return resp ,200
        else:
            return "Not Deployed",200
    else:
        return "parameter missing!!!",401  

def get_reference_image_util(data):
    print('data',data)
    mp = MongoHelper().getCollection('regions')
    mp_col = mp.find()
    
    resp = {}
    print(mp_col)
    if bool(data):
        parameter = data.get("parameter",None)
        for i in mp_col:
            print(i,'iiiiiiiii')
            region_name = i.get('region_name')
            image_count = i.get('fixed_images')
            print(region_name,image_count)

            resp[i.get('region_name')] = {'image_url':f"http://{IP_ADDRESS}:8001/reference_images/{region_name}/{region_name}.jpg", 'image_count':image_count}
        print(resp)
        return resp, 200
    else:
        return "None", 400

