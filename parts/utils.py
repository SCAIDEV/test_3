
from statistics import mode
from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId
from plan.utils import get_todays_planned_production_util
from common.utils import GetLabelData
import json

###############################################PART CRUDS#####################################


def add_part_details_task(data):
    try:
        model_number = data.get('model_number',None)
        model_detail = data.get('discription',None)
        mp = MongoHelper().getCollection("parts")
        isAnnotated = False
        isdeleted = False
        import datetime
        e = datetime.datetime.now()
        p = mp.find_one({'model_number': model_number})
        if not p:
            collection_obj = {
            'created_at': e.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': e.strftime("%Y-%m-%d %H:%M:%S"),
            'model_detail': model_detail,
            'model_number' : model_number,
            'isAnnotated': isAnnotated,
            'isdeleted' : isdeleted,
            }
            mp.insert_one(collection_obj)
            return model_number
        else:
            return 'part already exist'     
    except Exception as e:
        'part already exist ' + str(e)




def set_region_details_task(data):
    """
     {
	{"model_number":"avc","regions":[{"type":"box","x":0.4395231337006282,"y":0.23349189355055827,
    "w":0.1310782241014799,"h":0.06131078224101477,"highlighted":false,"editingLabels":false,
    "color":"#f44336","cls":"Country","id":"4196948742605484"},{"type":"box","x":0.2133074888803322,
    "y":0.21721281410523752,"w":0.05849189570119803,"h":0.07822410147991543,"highlighted":true,
    "editingLabels":true,"color":"#2196f3","cls":"MFD","id":"9054854791526026"}]}
    }
    """
    try:
        model_number = data.get('model_number',None)
        part_coordinates= data.get('regions',None)

        # print('********************************',part_coordinates)
        # kanban = data.get('kanban',None)
        isdeleted = False
        isAnnotated = True
        mp = MongoHelper().getCollection("parts")
        p = mp.find_one({'model_number': model_number})
        import datetime
        e = datetime.datetime.now()
        if p:
            p['isAnnotated'] = isAnnotated  
            p['updated_at']  = e.strftime("%Y-%m-%d %H:%M:%S")

            model_number = p.get('model_number')
            p['cordinates'] = part_coordinates
            mp.update_one({'_id' : p['_id']}, {'$set' :  p})
            return model_number
        else:
            return 'model number not found'

        # if not p:
        #     collection_obj = {
        #         'model_number' : model_number,
        #         'cordinates' : part_coordinates,
        #         'isdeleted' : isdeleted
        #         }
        
        #     mp.insert(collection_obj)
        # collection_obj = {
        #         'model_number' : model_number,
        #         'cordinates' : part_coordinates,
        #         'isdeleted' : isdeleted
        #         }
        
        #     mp.insert(collection_obj)
        # p['isdeleted'] = isdeleted        
        
        
    except Exception as e:
        return "Could not add part: "+str(e)


def delete_part_task(data):
    # _id = part_id
    id = data.get('_id')
    
    if id:
        mp = MongoHelper().getCollection("parts")
        pc = mp.find_one({'_id' : ObjectId(id)})
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.",pc)
        if pc:
            isdeleted = pc.get('isdeleted')
            if not isdeleted:
                pc['isdeleted'] = True
            mp.update_one({'_id' : ObjectId(pc['_id'])}, {'$set' :  pc})
            return data
        else:
            return "Part not found."


def update_part_task(data):
    """
  {"_id":"63592c01ca92b86afe9a9a49",
  "edit_model_number":"ankit23",
  "edit_model_description":"ksjdbvb"}
    """
    id = data.get('_id')
    if id:
        mp = MongoHelper().getCollection("parts")
        pc = mp.find_one({'_id' : ObjectId(id)})
        if pc:
            import datetime
            e = datetime.datetime.now()
            pc['updated_at']  = e.strftime("%Y-%m-%d %H:%M:%S")
            updated_number = data.get('edit_model_number',None)
            part_description = data.get('edit_model_description',None)
            # kanban = data.get('kanban',None)
            # if part_number:
            pc['model_number'] = updated_number
            pc['model_detail'] = part_description
            
            mp.update_one({'_id' : pc['_id']}, {'$set' :  pc})
        else:
            return "Part not found"
        return "Updated Successfully"
    else:
        return "Please enter the part ID."
    

        

def get_part_details_task(part_id):
    mp = MongoHelper().getCollection("parts")
    p = mp.find_one({'_id' : ObjectId(part_id)})
    if p:
        return p
    else:
        return {}

def get_all_part_details_task():
    mp = MongoHelper().getCollection("parts")
    parts =[p for p in  mp.find({'isdeleted' : False})]
    # print('>>>>>',parts)
    parts_data = []
    
    for p in parts:
        part= {}
        part['model_number'] = p.get('model_number')
        part['isAnnotated'] = p.get('isAnnotated')
        part['_id']=p.get('_id')
        parts_data.append(part)
    if parts_data:
        return {'parts_data': parts_data[::-1]}
    else:
        return {}

def get_all_part_type_util():
    try:
        mp = MongoHelper().getCollection("parts_type")
        parts =[p for p in  mp.find({'isdeleted' : False})]
        parts_data = []

        for p in parts:
            parts_data.append(p.get('part_type'))
        if parts_data:
            return {'parts_data': parts_data}
        else:
            return {}
    except Exception as e:
        print(e)

    

# def get_parts_task():
#     mp = MongoHelper().getCollection("parts")
    
#     parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).sort( "$natural", -1 )]

#     for i in parts:
#         data = {}
#         part_obj_id = i["_id"]
#         mp = MongoHelper().getCollection('experiment')
#         i["experiments"] = [i for i in mp.find({'part_id' : str(part_obj_id)})]
#         info = GetLabelData(part_obj_id).get_metrics()
#         i["label_info"] = info
#     if parts:
#         return parts
#     else:
#         return []

######################################TBAL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def get_configuration_list_util():
    #Get Configuration collection list
    mp = MongoHelper().getCollection(CONFIGURATION_COLLECTION)
    conf_list = []
    cc = mp.find({"in_use":True})
    for c in cc :
        conf_list.append(c["configuration_number"])
    return conf_list

def get_aircraft_number_new_util():
    mp = MongoHelper().getCollection(AIRCRAFT_NUMBER_COLLECTION)
    ac_num_list = []
    cc = mp.find({"is_used":False})#inprogress,completed
    for c in cc :
        ac_num_list.append(c["aircraft_number"])
    return ac_num_list

def get_aircraft_number_used_util():
    mp = MongoHelper().getCollection(AIRCRAFT_NUMBER_COLLECTION)
    ac_num_list = []
    cc = mp.find({"is_used":True})#inprogress,completed
    for c in cc :
    #     print(c)
        ac_num_list.append(c["aircraft_number"])
    return ac_num_list

# def get_aircraft_number_completed_util():
#     mp = MongoHelper().getCollection(AIRCRAFT_NUMBER_COLLECTION)
#     ac_num_list = []
#     cc = mp.find({"status":"completed"})#inprogress,completed
#     for c in cc :
#     #     print(c)
#         ac_num_list.append(c["aircraft_number"])
#     return ac_num_list

# def get_aircraft_number_inprogress_completed_util():
#     mp = MongoHelper().getCollection(AIRCRAFT_NUMBER_COLLECTION)
#     ac_num_list = []
#     cc = mp.find({"$or" :[{"status":"completed"},{"status":"inprogress"} ]})#inprogress,completed
#     for c in cc :
#     #     print(c)
#         ac_num_list.append(c["aircraft_number"])
#     return ac_num_list


def get_region_task(data):
    try:
        part_id = data.get('_id')
        mp = MongoHelper().getCollection('parts')
        p = mp.find_one({'_id' : ObjectId(part_id)})
        if p:
            return p['cordinates']
        else:
            return 'something'

    except Exception as e:
        print(e)


def get_progress_details():
    try:
        mp = mp = MongoHelper().getCollection('master_file')
        p = mp.find_one()
        return len(p)
    except Exception as e:
        print(e)