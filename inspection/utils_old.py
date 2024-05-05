from common.utils import CacheHelper,MongoHelper
from django.http import response
import inspection
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
import datetime
from dateutil import tz
import requests
# import datetime
from datetime import datetime
# from mongohelper import MongoHelper
from base64 import decodebytes
import pandas as pd
import os
from pyzbar.pyzbar import decode
from PIL import Image
# import datetime
from paddleocr import PaddleOCR
from paddleocr import PaddleOCR



#### Directory for images
img_path=os.path.join('d:/images/')


#calculate cuurent month 

def getMonth(year: int, week: int) -> int:
    month=str( datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").month)
    datetime_object = datetime.strptime(month, "%m")
    full_month_name = datetime_object.strftime("%B")

    return full_month_name

# print(getMonth(2018, 23))

def denormalize(coords,imgsize,im,cls):
    height ,width= imgsize
    x0 = int(coords[0] * width)
    y0 = int(coords[1] * height)
    x1 = int((coords[0]+coords[2])* width)
    y1 = int((coords[1]+coords[3]) * height)
    new_img = im[y0:y1,x0:x1]
    path = '../{}.jpg'.format(cls)
    # print("////////////",path)
    cv2.imwrite(path,new_img)
    return path


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

#   ocr = PaddleOCR(
    
#     )


@singleton
class OCR():
    def __init__(self):
        self.PDOCR = PaddleOCR(use_angle_cls=True,
    lang='en', 
    table=False, 
    use_mp=True,
    # image_dir='ocr_images',
    enable_mkldnn=True,
    use_gpu=False,
    max_batch_size = 20,
    total_process_num = os.cpu_count() * 2 - 1,)
        img = np.zeros((640,480,3))
        self.PDOCR.ocr(img)

    def predict(self, frame):
        return self.PDOCR.ocr(frame)



ocr_model = OCR()


def ocr_status_details(img_path,country_db):
        mp_country = MongoHelper().getCollection("country_code")
    #try:
        m=time.time()
        #ocr = PaddleOCR(lang='en',use_gpu=True)
        # img_path ="D:\images\img_6368b67a2e7f89bb029bbd4f.jpg"
        # regions = regions
        # frame =cv2.imread(img_path)
        # print("SIZE OF FRAME : : : : : : : : : : : : : : : : :",frame.shape)
        # # frame = cv2.resize(frame,(640,480))
        result = ocr_model.predict(img_path)
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",result)
        end_time=time.time()
        
        # result = ocr.ocr(img_path,cls=False)
        print("Time taken for model loading and infrencing is ",end_time-m)
        # from re import search
        val  = "made"
        ctr=False
        prediction = []
        for line in result:
            for j in line:
                
                prediction.append(j[-1][0].replace(" ",""))
                # if val not in j[-1][0].lower():
                #     break
                if val in j[-1][0].lower():
                    ctr=True
                    print("HEY COUNTRY IS FOUND %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        
        if ctr==False:
            date_list=[]
            date_list.append("1")
        elif ctr==True:

            val  = "made"
            ctr=False
            prediction = []
            for line in result:
                for j in line:
                    
                    prediction.append(j[-1][0].replace(" ",""))
                    # if val not in j[-1][0].lower():
                    #     break
                    if val in j[-1][0].lower():
                        ctr=True

                        print("great we found it ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                        country = (j[-1][0].split(' ')[-1])
                        if 'chin' in country.lower():
                            country = 'China'
                        elif 'indo' in country.lower():
                            country = 'Indonesia'
                        elif 'viet' in country.lower():
                            country = 'Vietnam'

                        else:
                            country = country

            print("Country is <<<<<<<<<<<<",country)
            
            # else:    
            country_list = [i for i in mp_country.find({'Country of origin':country_db})]
            print('>>>>>>>>>>>>>>>>',prediction)
            country_code = set()
            len_date_format = []
            year_code = []
            for i in country_list:
                date_format = (i['Maufacturing date code format']).replace(" ","")
                len_date_format.append(len(date_format))
                country_code.add((i['Maufacturing date code format']).replace(" ","")[:2])
                year_code.append((i['Maufacturing date code format']).replace(" ",""))
                print(len_date_format)
            print('>>>>>>>>>>>>>>>>>>',year_code)
            further_val  = []
            for pred in prediction:
                for l in len_date_format:
                    if l == len(pred):
                        further_val.append(pred)

            print('&&&&&&&&&&&&&&&&&&&&&&&&',further_val)
            final_val = set()
            for fthr_val in further_val:
                for cnt_code in country_code:
                    if cnt_code == fthr_val[:2]:
                        final_val.add(fthr_val)
            
                    
            final_val = list(final_val)
            print('zzzzzzzzzzzzzzzzzzz4zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',final_val)
            date_list = []
            for fin in final_val:
                for year in year_code:
                    if len(year) == len(fin):
                        if "MONTH" in year:
                            work_year = year[2:-1]
                            work_month = year[:3]
                            # date_list.append(work_year)
                            # date_list.append(work_month)
                            # print(">>>>>>>>>>>>>>>>>>>>>>",year)
                            # print("<<<<<<<<<<<<<<<<<<<<<<",fin)
                        else:
                            target_y = "Y"
                            start_position_Y = year.index("Y")
                            last_pos_Y = len(year) - 1 - year[::-1].index(target_y)
                            work_year = fin[start_position_Y:last_pos_Y+1]


                            start_position_w = year.index("W")
                            target_w = "W"
                            last_pos_w = len(year) - 1 - year[::-1].index(target_w)
                            # last_pos_hyphon = len(year) - 1 - year[::-1].index(target_w)
                            

                            if start_position_w == last_pos_w:
                                work_week = fin[start_position_w+1:start_position_w+3]
                            else:
                                work_week = fin[start_position_w:last_pos_w+1]

                        


                        date_list.append(work_year)
                        date_list.append(work_week)
            print("date list id 8888888888888888*****************************",date_list)

            return date_list
    #except Exception as e:
    #    print(e)


def get_running_process_utils():
    try:
        mp = MongoHelper().getCollection('inspection')
        
        insp_coll = [i for i in mp.find()]
        inspection_id = ""
        response = {}
        if len(insp_coll) > 0:
            res = insp_coll[-1]
            if res["status"]=="started":
                print("stat ids dddddddddd",res)

                response["inspection_id"] = str(res['_id'])

            else:
                pass    
    except Exception as e:
        print(e)
        
        # print("*****************Running process inspection_id*********************",inspection_id)
    return response,200


def get_current_utils():
    try:
        mp = MongoHelper().getCollection('Current_inspection')
        
        insp_coll = [i for i in mp.find()]
        inspection_id = ""
        response = {}
        if len(insp_coll) > 0:
            res = insp_coll[-1]
            if res["state"]=="started":
                print("stat ids dddddddddd",res)

                response =res

            else:
                pass    
    except Exception as e:
        print(e)
        
        # print("*****************Running process inspection_id*********************",inspection_id)
    return response,200



def barcode_scanner(image):
    
    try:
        img=cv2.imread(image)
        print("image",img)
        #     return e 
        # if img:

        # print("img",img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
        q2c_barcode = ""
        p = decode(img)
        print(p)
        

        if p:
            k = p[0][0]
            q2c_barcode = (k.decode('UTF-8'))
            print("TYPE OG HUSGFGJSGJKSGD&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",type(q2c_barcode))
            return q2c_barcode
        else:
            return  None
    except Exception as e:
        return e
def get_manufacturing_date(image):
    original_image=image
    # cordinate=cordinates
    payload =  {"original_image":original_image}
            
    try:    
        print("before hitting ")
        response = requests.post('http://127.0.0.1:9004', json = payload)
        print(response.text)
    except requests.exceptions.HTTPError as errh:
        print(errh)
       
        return errh
    except requests.exceptions.ConnectionError as errc:
        
        print(errc)
        return errc
    except requests.exceptions.Timeout as errt:
        
        print(errt)
        return errt
    except requests.exceptions.RequestException as err:
      
        print(err)
        return err
    except Exception as e:
        
        return e    

    mfg_date = []

    for doc in response.json():
        for j in doc:
            mfg_date.append(doc)
    return mfg_date        




def start_process_util(data):
    try:
        rch=CacheHelper()

        createdAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        createDate = datetime.now().strftime("%Y-%m-%d")
        COLL_NAME = "INSPECTION_"+datetime.now().strftime("%m_%y")
        mp = MongoHelper().getCollection("inspection")
        # print("mpis %%%%%%%%%%%%%%%%%%%%%%",mp)

        obj={
            'start_time':createdAt,
            'created_date':createDate,
            "status":"started"


        }
        _inspection_id = mp.insert_one(obj)
        # _inspection_id=mp.insert(obj)
        # print("id is ",_inspection_id)
        return "succes",200
    except Exception as e:
        return e

def current_inspection():
    return id

def start_inspection_util(data):
    # try:
        process_start_time=time.time()
        rch=CacheHelper()
        inspection_id=data.get("inspection_id",None)
        if inspection_id is not None:
            createdAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            createDate = datetime.now().strftime("%Y-%m-%d")
            COLL_NAME = "INSPECTION_"+datetime.now().strftime("%m_%y")
            mp = MongoHelper().getCollection("inspection_"+str(inspection_id))
            mp2=MongoHelper().getCollection("Current_inspection")
            
            
            obj={
                'start_time':createdAt,
                'created_date':createDate
            }
            _inspection_id=mp.insert_one(obj).inserted_id
            iid=mp2.insert_one(obj).inserted_id
            # print("inspection id is $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",COLL_NAME)
           
            start_time_check_bottom1 = time.time()
            rch.set_json({'camera_original':None})
            rch.set_json({'camera_trigger':True})
            while True:
                # time.sleep(1.5)
                bottom_one_write = rch.get_json('camera_original')
                if bottom_one_write is not None:
                    print('Read the image')
                    rch.set_json({'camera_original':None})
                    break
                if time.time() - start_time_check_bottom1 > 20:
                    break
            image_name="img_"+str(_inspection_id)+".jpg"
            # "D:\images\img_6368b67a2e7f89bb029bbd4f.jpg"
            # image_name='img_6368b67a2e7f89bb029bbd4f.jpg'
            
            
            captured_img_pth1 = os.path.join(img_path,image_name)
            # print("image_path",captured_img_pth1)
            # print("images is",bottom_one_write)
            # bottom_one_write=cv2.resize(bottom_one_write,(1000,1000),interpolation = cv2.INTER_LINEAR)
            print("image_path",captured_img_pth1)
            cv2.imwrite(captured_img_pth1,bottom_one_write)
            print("DONE WITH IMAGE WRITE")

            #----------------------->>>>>>>>>>>>>>>>>>>> img path for testing
            # captured_img_pth1 = "D:\images\img_6374efa7a32b3ba801a344a5.jpg"
            # captured_img_pth1 = img_path
            #_--------------------------------------->>>>>>>>>>>>>>


            time_taken_in_image_captur=time.time()-start_time_check_bottom1
            print("TIME TAKEN IN IMAGE TAKEN AND WRITING ON DISK IS *****************************",time_taken_in_image_captur)   
            start_time_for_pyzbar=time.time()
            

            eu_number=barcode_scanner(captured_img_pth1)
            
            time_taken=start_time_for_pyzbar-time.time()
            print("TIME TAKEN IN PYZBAR $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",time_taken)
            # print(eu_number)
            if  eu_number:
                print("eu is            ----------------------",eu_number)
                eu_number = eu_number.replace(" ","")
                mp_1=MongoHelper().getCollection("master_file")
                # mp_2 =MongoHelper().getCollection("parts")
                doc =  mp_1.find_one({'EAN':str(eu_number)})
                print("DOc9999999999999999999999999999",doc)
                if doc is None:
                    res={}
                    message="NO RECORD FOUND FOR THIS EU NUMBER"
                    status1={"isvalid":False}
                    status=400
                    return res,status1,message,status 

                   
                      
                else:
                    model_num =  doc['Material']
                    amount=doc['Amount']
                    country_db=doc['Country of Origin']
                    description=doc["Material description"]
                    # nextstep = True
                    # model_num = []
                    # amount = []
                    # country_db = []
                    # nextstep = False
                start_time=time.time()    
                date_list=ocr_status_details(captured_img_pth1,country_db)
                print("result from ocr is %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",date_list)
                # print("result from ocr is %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",len(date_list))
                time_for_paddle_ocr=time.time()-start_time
                print("Time Taken FOR PADDLE OCR IS ",time_for_paddle_ocr)
                if date_list is None:
                    print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                    res={}
                    message="UNABLE TO READ OCR"
                    status=400
                    status1={"isvalid":False}
                    return res,status1,message,status 
                elif len(date_list)==1:
                    print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                    res={}
                    message="No Country aavailable"
                    status=400
                    status1={"isvalid":False}
                    return res,status1,message,status 
                elif len(date_list)==0:
                    print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                    res={}
                    message="No Country aavailable"
                    status=400
                    status1={"isvalid":False}
                    return res,status1,message,status     


                else:

                        
                    print("<<<<<<<<<<<<<<<<<<<<<<",date_list)
                    if len(date_list[-2]) == 2:
                        date_year=str(20)+date_list[-2] 
                    else:
                        date_year = str(date_list[-2])
                    date_week=date_list[-1]
                    month=getMonth(int(date_year),int(date_week))
                    print("month is ]]]]]]]]]]]]]]]]",month)
                    mfg_date=month+"  "+date_year
                    image_url='http://localhost:3306/'+image_name
                    mp.update_one({'_id':ObjectId(_inspection_id)}, {"$set": { "Model_number":model_num,"Manufacturing_date":mfg_date,"Copies":1,"Quantities":1,"EU13":eu_number,'Amount':amount ,"country":country_db,"status":"Accepted","image_url":image_url,"description":description,"operator":"operator1"}},upsert=True)
                    mp2=MongoHelper().getCollection("Current_inspection")
                    mp2.update_one({'_id':ObjectId(iid)}, {"$set": { "Model_number":model_num,"Manufacturing_date":mfg_date,"Copies":1,"Quantities":1,"EU13":eu_number,'Amount':amount ,"country":country_db,"status":"Accepted","image_url":image_url,"state":"started"}},upsert=True)

                    res={ "model_number":model_num,"mfg_date":mfg_date ,"eu_number":eu_number,"image_url":image_url,"inspection_id":_inspection_id,"image_url":image_url,"status":"Accepted","copies":1,"qunatity":1}
                    total_process_time=process_start_time-time.time()
                    print("total time taken in processing is ",total_process_time)
                    status1={"isvalid":True}
                    return res,status1,"success",200
                # else:
                #     res={}
                #     message="UNABLE TO READ OCR"
                #     status=400
                #     status1={"isvalid":False}
                #     return res,status1,message,status  
                            
                
            
                
            else:
                res={}
                message="NO BAR CODE AVAILABLE ON LABEL"
                status=400
                status1={"isvalid":False}
                return res,status1,message,status    

    # except Exception as e:
    #         return e,"Something went Wrong",400
            
    #         eu_number=eu_number.replace(' ','') 
          

    
        

                    









# def start_inspection_util(data):
#     try:
#         rch=CacheHelper()
#         inspection_id=data.get("inspection_id",None)
#         if inspection_id is not None:
#             createdAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             createDate = datetime.now().strftime("%Y-%m-%d")
#             COLL_NAME = "INSPECTION_"+datetime.now().strftime("%m_%y")
#             mp = MongoHelper().getCollection("inspection_"+str(inspection_id))
#             obj={
#                 'start_time':createdAt,
#                 'created_date':createDate
#             }
#             _inspection_id=mp.insert_one(obj).inserted_id
#             print("inspection id is $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",COLL_NAME)
        

#             # start_time_check_bottom1 = time.time()
#             # rch.set_json({'bottom_three_original':None})
#             # rch.set_json({'camera_bottom_three_trigger':True})
#             # while True:
#             #     # time.sleep(1.5)
#             #     bottom_one_write = rch.get_json('bottom_three_original')
#             #     if bottom_one_write is not None:
#             #         print('Read the image')
#             #         rch.set_json({'bottom_three_original':None})
#             #         break
#             #     if time.time() - start_time_check_bottom1 > 26:
#             #        break
#             # bottom_one_write = rch.get_json('bottom_one_original')
#             # image_name="img_"+str(_inspection_id)+".jpg"
#             # "D:\images\img_6368b67a2e7f89bb029bbd4f.jpg"
#             image_name='img_6368b67a2e7f89bb029bbd4f.jpg'
           
#             captured_img_pth1 = os.path.join(img_path,image_name)
#             # print("image_path",captured_img_pth1)
#             # print("images is",bottom_one_write)
#             # cv2.imwrite(captured_img_pth1,bottom_one_write)


#             eu_number=barcode_scanner("D:\images\img_6368b67a2e7f89bb029bbd4f.jpg")
#             print("EUBBBBBBBBBBBBBBBBBB",eu_number)
            

#             mp_1=MongoHelper().getCollection("master_file")
#             mp_2 =MongoHelper().getCollection("parts")
#             doc =  mp_1.find_one({'EAN':eu_number})
#             if doc:
#                 model_num =  doc['Material']
#                 amount=doc['Amount']
#                 country_db=doc['Country of Origin']
#                 nextstep = True
#             # print(doc)
#             # for i ,j in doc.items():
#             #     # print("...........",type(j))
#             #     if j["EAN"] == eu_number:      
#             else:
#                 model_num = []
#                 amount = []
#                 country_db = []
#                 nextstep = False

#             if nextstep:
#                 coordinates =  mp_2.find_one({'model_number':model_num})
#                 region_corr = coordinates['cordinates']
#                 val_dict = ocr_status_details(captured_img_pth1,regions=region_corr)
#                 mfg_date=val_dict["MFD"].replace(" ", "")
#                 Country=val_dict['Country']
#                 date_year,date_week=str(20)+(mfg_date.split()[0])[2:4],(mfg_date.split()[0])[4::]
#                 month=getMonth(int(date_year),int(date_week))
#                 print("month is ",month)
#                 mfg_date=month+" "+date_year

#                 if Country.upper()==country_db.upper():
#                     Status="Accepted"
#                 else:
#                     Status="Rejected"

#                 image_url='http://localhost:3306/'+image_name
#                 mp.update_one({'_id':ObjectId(_inspection_id)}, {"$set": { "Model_number":model_num,"Manufacturing_date":mfg_date,"Copies":1,"Quantities":1,"EU13":eu_number,'Amount':amount ,"country":Country,"status":Status,"image_url":image_url}},upsert=True)


#             res={ "model_number":model_num,"mfg_date":mfg_date ,"eu_number":eu_number,"image_url":image_url,"inspection_id":_inspection_id,"image_url":image_url,"status":Status}
                
#             return res,200
#     except Exception as e:
#         return e , 400




def submit_process_util(data):
    try:
        l=[]
        model_number=data.get("model_number",None).upper()
        print("mOdel_number",model_number)
        eu_13=data.get("eu_number",None)
        print("eu_13 is ",eu_13)

        mfg_date=data.get("mfg_date",None)
        print("mfg is ",mfg_date)

        quanatity=data.get("quantities",None)
        print("qudsjdb is ",quanatity)

        copies=data.get("copies",None)
        print("copies is ",copies)

        
        # amount=int(quanatity)*int(copies)
        _id=data.get("inspection_id",None)
        print("id is ",_id)
        # description=data.get("description")

        createdAt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        createDate = datetime.now().strftime("%Y-%m-%d")

        
            
        
        mp = MongoHelper().getCollection("inspection_"+str(_id))
        insp_coll = [i for i in mp.find()]
        act={}
        edited={}
        if len(insp_coll) > 0:
            ins=insp_coll[-1]
            act["Model_number"]=ins["Model_number"]
            act["Manufacturing_date"]=ins["Manufacturing_date"]
            act["Copies"]=ins["Copies"]
            act["Quantities"]=ins["Quantities"]
            act["EU13"]=ins["EU13"]
            act["Amount"]=ins["Amount"]
            __id=ins["_id"]
            description=ins['description']

            amount=ins['Amount']
            country=ins["country"]
            # { "Model_number":"123","Manufacturing_date":"12/2/2222","Copies":1,"Quantities":1,"EU13":14141 }
            


        else:
            act["Model_number"]=insp_coll["Model_number"]
            act["Manufacturing_date"]=insp_coll["Manufacturing_date"]
            act["Copies"]=insp_coll["Copies"]
            act["Quantities"]=insp_coll["Quantities"]
            act["EU13"]=insp_coll["EU13"]
            amount=ins['Amount']
            act["Amount"]=ins["Amount"]
            description=ins['description']
            
            country=ins["country"]
            __id=ins["_id"]
            
            

        amount_= int(amount)*int(quanatity)
        print("sgdjasdgfjhsdagffffffffffffjasd",insp_coll)
        if act['Model_number'].upper()==model_number.upper():
            edited['Model_number']=""
        else:
            edited['Model_number']=model_number
        if act['Manufacturing_date']==mfg_date:
            edited['Manufacturing_date']=""
        else:
            edited['Manufacturing_date']=mfg_date
        if int(act['Copies'])==int(copies):
            edited['Copies']=""
        else:
            edited['Copies']=copies
        if int(act['Quantities'])==int(quanatity):
            edited['Quantities']=""
        else:
            edited['Quantities']=quanatity


        if int(act['EU13'])==int(eu_13):
            edited['EU13']=""
        else:
            edited['EU13']=eu_13


        
        if int(act['Amount'])==int(amount_):
            edited['Amount']=""
        else:
            edited['Amount']=amount_

        # if (act['description'])==description:
        #     edited['description']=""
        # else:
        #     edited['description']=description


        




        mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited}},upsert=True)


        

        preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":amount_,"Country":country,"description":description}
        mp2=MongoHelper().getCollection("Current_inspection")
        mp2.update_one({'_id':ObjectId(__id)}, {"$set": {"state": "completed"}})

        return act,edited,preview,200
        # else:
        #     act={1:1}
        #     edited={1:1}
        #     preview={2:2}

        #     act=[],edited=[],preview=[],401

    except Exception as e:
        return e , 400


def print_inspection(data):
    l=[]
    amount=data.get("Amount")
    
    country=data.get("Country")
    
    createdAt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    createDate = datetime.now().strftime("%Y-%m-%d")

    model_number=data.get("Model_Number")

    mfg_date=data.get("Manufacturing_date")
    quanatity=data.get("Quantities")
    copies=data.get("Copies")
    
    l.extend(["Date;MRP;Origin;Model;Qty;Copy" '\n',str(mfg_date)+";"+str(amount)+";"+str(country)+";"+str(model_number)+";"+str(quanatity)+";"+str(copies)])
    file1 = open("D:/PRINT_TEXT_FILES/"+str(createdAt)+".txt","w")
    file1.writelines(l)
    file1.close()
    # mp=MongoHelper().getCollection("Current_inspection")
    # mp.update_one({'_id':ObjectId(inspection_id)}, {"$set": {"status": "completed"}})
    return 200





    

def end_process_util(data):
    #from datetime import datetime
    inspection_id  = data.get('inspection_id', None)

    
    mp = MongoHelper().getCollection("inspection")
    
 
    mp.update_one({'_id':ObjectId(inspection_id)}, {"$set": {"status": "completed"}})
  

    return "Success",200

def update_file_details(data):
    try:
        mp = MongoHelper().getCollection('master_file')
        mp1 = MongoHelper().getCollection('mini_master')
        insp_coll = [i for i in mp.find()]
        file = data.FILES.get('file')
        
        
        df = pd.read_excel(file,'SEIPL',engine='openpyxl')

        if 'EAN' and 'Material'and 'Material description'and 'Amount' and 'Unit' and 'UoM' and 'Country of Origin' in df:
            df1 = df[['EAN','Material','Material description','Amount','Unit','UoM','Country of Origin']]
            df1['C'] =(np.arange(len(df1)))
            df1=df1.applymap(str)
            df1["Uploaded By"]="operator1"
            df1["Upload Date"]=datetime.now().strftime("%Y-%m-%d")
            dist =df1.set_index((df1['C'])).T.to_dict()
            # df2 = pd.DataFrame(df1['EAN'].apply(str))
            # # df2['eu-number'] = 
            # dist =df1.set_index(df2['EAN']).T.to_dict()
            valuesList = list(dist.values())

            if len(insp_coll)==0:
                mp1.insert_one(dist)
                mp.insert_many(valuesList)
            else:
                previous_dict = mp1.find_one()
                previous_dict.update(dist)
                mp1.drop()
                mp1.insert_one(previous_dict)
                new_list =list(previous_dict.values())
                new_list = new_list[1:]
                mp.drop()
                mp.insert_many(new_list)

        #sheet 2----------------------------------------------------------------------->>>>>>>>>>>>>>>>
            sheet2 = pd.read_excel(file,'Sheet2',engine='openpyxl')
            sheet2['C'] =(np.arange(len(sheet2)))
            sheet2=sheet2.applymap(str)
            dist2 =sheet2.set_index((sheet2['C'])).T.to_dict()
            # print(dist2)
            mp2 = MongoHelper().getCollection('country_code')
            mp3 = MongoHelper().getCollection('mini_country')
            insp_coll2 = [i for i in mp3.find()]
            valuesList2 = list(dist2.values())
            if len(insp_coll2)==0:
                mp3.insert_one(dist2)
                mp2.insert_many(valuesList2)
            else:
                # print('888888888',type(mp.find_one()))
                previous_dict1 = mp3.find_one()
                previous_dict1.update(dist2)
                mp3.drop()
                mp3.insert_one(previous_dict1)
                new_list1 =list(previous_dict1.values())
                new_list1 = new_list1[1:]
                mp2.drop()
                mp2.insert_many(new_list1)


            message = "success"
        else:
            message = 'Wrong sheet/ Required column not available'
        return message , 200
    except Exception as e:
        return e , 400

    

def get_master_file_details(data):

    try:
        mp = MongoHelper().getCollection('master_file')
        part_list = [i for i in mp.find()]
        if len(part_list)==0:
            part_list=[]
            return part_list,200
        else:

            return part_list , 200
    except Exception as e:
        print(e)



def health_check_details(data):
    # try:
        result = {}
        rch = CacheHelper()
        cam_checker = rch.get_json('camera_original')
        if cam_checker is None:
            feed = False
        else :
            if len(cam_checker) == 0:
                feed = True
            else:
                feed = True
        result['camera'] = feed
            
        return result , 200
        
    # except Exception as e:
    #     print(e)


