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
    # import datetime

    # x = datetime.datetime.now()
    # from datetime import datetime

    current_dateTime = datetime.now()
    # print(x.year)
    if week>53 :
        
        return 0
    elif year > current_dateTime.year : 
        return 0   
    else:

# or int( datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").month) > int(current_dateTime.month)
        month=str( datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").month)
        year=str( datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").year)

        print("hey month is ,,,,,,,,,,,,,,,,,,,,****************///////////",month)
        if len(month)==1:
            month=str(0)+month

        return month

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
            print("************************************************************")
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
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                
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

                    # print("Country is <<<<<<<<<<<<",country)
            stat_="Accepted"
            # if country==country_db:
            #     stat_="Accepted"
            
            # else:    
            country_list = [i for i in mp_country.find({'Country of origin':country_db})]
            print('>>>>>>>>>>>>>>>>pderdiction',prediction)
            # print("country list ",country_list)
            country_code = set()
            len_date_format = []
            year_code = []
            for i in country_list:
                date_format = (i['Maufacturing date code format']).replace(" ","")
                len_date_format.append(len(date_format))
                country_code.add((i['Maufacturing date code format']).replace(" ","")[:2])
                year_code.append((i['Maufacturing date code format']).replace(" ",""))
            print("llllllllllllllllllllllllllll",date_format)
            print('>>>>>>>>>>>>>>>>>>year code--------',len_date_format)
            further_val  = []
            for pred in prediction:
                for l in len_date_format:
                    if l == len(pred):

                        further_val.append(pred)

            print('&&&&&&&&&&&&&&&&&&&&&&&& further value',further_val,country_code)
            if country_db.lower()=="mexico":
                date_list=[]
            
                pass 

            final_val = set()
            for fthr_val in further_val:
                print("////////////////////",fthr_val)
                for cnt_code in country_code:
                    print("////////////////////",cnt_code)

                    if cnt_code == fthr_val[:2]:
                        final_val.add(fthr_val)
                    # else:


            
                    
            final_val = list(final_val)
            print("Finaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",final_val)
            print("Finaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",len(final_val))

            if len(final_val)==0:
                # pass
                print("inside n0000000000000000000000000000000000000000000000000000")
                return None,None,None,None

            # print('zzzzzzzzzzzzzzzzzzz4zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',final_val)4
            else:

                date_list = []
                for fin in final_val:
                    for year in year_code:
                        # print()
                        if len(year) == len(fin):
                            year_format = year
                            # print('yearrrrrrrrrrrrrrrrcodeeeeeeeeeeeeeee',year)
                            if "MONTH" in year:
                            
                                work_year = year[2:-1]
                                work_month = year[:3]
                                from datetime import datetime
                                mnum = datetime.strptime(work_month, '%B').month

                                import datetime
                                date = datetime.date(work_year,mnum,1)
                                year_week = date.strftime('%Y-%V')
                                work_week = (year_week.split('-')[-1])
                                # work_year
                            elif country_db.lower() == 'china' and 'WX' in fin:
                                # print('coronaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                                target_y = "Y"
                                start_position_Y = year.index("Y")
                                last_pos_Y = len(year) - 1 - year[::-1].index(target_y)
                                work_year = fin[start_position_Y:last_pos_Y+1]

                                target_w = "W"
                                last_pos_w = len(year) - 1 - year[::-1].index(target_w)
                                work_week = fin[last_pos_w+1:last_pos_w+3]
                                
                            else:
                                print("in else block")
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
                # print("date list id 8888888888888888*****************************",date_list)
                # date_l=[]
                # date_l.append()
                # print('????????????????????????????????',year)
                print("hey fial vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",date_list)
                if len(final_val)==0:
                    final_val=None
                    print("year frrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",year_format)

                else:
                    final_val=final_val[0]
                    dat=[]
                    dat.append(date_list[-2])
                    dat.append(date_list[-1])
            
                return stat_,final_val,dat,year_format
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
        import cv2
        import zxingcpp

# img = cv2.imread('e:n.jpg')
# if results:
        img=cv2.imread(image)
        print("image",img)
        #     return e 
        # if img:

        # print("img",img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
        q2c_barcode = ""
        p = decode(img)
        results = zxingcpp.read_barcodes(img)

        print(p)
        

        if p:
            lm = []
            for i in p:
                k = i[0]

                q2c_barcode = (k.decode('UTF-8'))
                lm.append(q2c_barcode)
                print("TYPE OG HUSGFGJSGJKSGD&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",type(q2c_barcode))
            return lm
        elif results:
            lm = []
            for i in results:
                # k = i[0]

                # q2c_barcode = (k.decode('UTF-8'))
                lm.append(results.text)
                print("TYPE OG HUSGFGJSGJKSGD&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",type(q2c_barcode))
            return lm


        else:
            return  None
    except Exception as e:
        return e



def start_process_util(data):
    try:
        rch=CacheHelper()

        createdAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        createDate = datetime.now().strftime("%d-%m-%Y")
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


def start_inspection_util(data):
    # try:
        process_start_time=time.time()
        rch=CacheHelper()
        inspection_id=data.get("inspection_id",None)
        user=data.get("user")
        user_name=user["username"]
        label_type=data.get("label_type")
        font_size=data.get("font_size")
        if inspection_id is not None:
            createdAt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            createDate = datetime.now().strftime("%d-%m-%Y")
            COLL_NAME = "INSPECTION_"+datetime.now().strftime("%m_%y")
            mp = MongoHelper().getCollection("inspection_"+str(inspection_id))
            mp2=MongoHelper().getCollection("Current_inspection")

            # coll=mp2.find_one({"_id":ObjectId("636e8d2bfe4f1e6b24123734")})
            
            # iid="636e8d2bfe4f1e6b24123734"
            # iid=coll["_id"]
            # print("collection iuuuuuuuuuuuuuuuuuUUUU((((((((((((((()))))))))))))))))0",coll)
            # print("collection is6666666666666666666666666^^^^^^^^^^^^^^^^^^^^^^^^^66 ",iid)
            
            
            obj={
                'start_time':createdAt,
                'created_date':createDate,
                "label_type":label_type,
                "font_size":font_size
            }
            _inspection_id=mp.insert_one(obj).inserted_id

            mp2=MongoHelper().getCollection("Current_inspection")

            ## for cuRRENT 
            if mp2 is None:
                iid=mp2.insert_one(obj)
                print("ID FOR CURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRNT INSPECTION IS ",iid)
            else:
                id=[ i for i in mp2.find()]
                id=id[-1]
                iid=id["_id"]
                print("ID FOR CURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRNT INSPECTION IS ",iid)

                mp2.update_one({'_id':ObjectId(iid)}, {"$set":{'start_time':createdAt,'created_date':createDate }},upsert=True)
                print("ID FOR CURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRNT INSPECTION IS ",iid)


            # mp2.update_one({'_id':ObjectId(iid)}, {"$set": { "Model_number":model_num,"Manufacturing_date":mfg_date,"Copies":1,"Quantities":1,"EU13":eu_number,'Amount':amount ,"country":country_db,"status":"Accepted","image_url":image_url,"state":"started"}},upsert=True)

            # print("inspection id is $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",COLL_NAME)
           
            start_time_check_bottom1 = time.time()
            rch.set_json({'camera_original':None})
            rch.set_json({'camera_trigger':True})
            while True:
                # time.sleep(1.5)
                bottom_one_write = rch.get_json('camera_original')
                if bottom_one_write is not None:
                    print('Read the image')
                    # rch.set_json({cam_health:})
                    rch.set_json({'camera_original':None})
                    break
                if time.time() - start_time_check_bottom1 > 20:
                    break
            image_name="img_"+str(_inspection_id)+".jpg"
            # "D:\images\img_6368b67a2e7f89bb029bbd4f.jpg"
            # image_name='img_6368b67a2e7f89bb029bbd4f.jpg'
            
            
            captured_img_pth1 = os.path.join(img_path,image_name)
            # print("image_path",captured_img_pth1)
            print("images is",bottom_one_write)
            # bottom_one_write=cv2.resize(bottom_one_write,(1000,1000),interpolation = cv2.INTER_LINEAR)
            print("image_path",captured_img_pth1)
            cv2.imwrite(captured_img_pth1,bottom_one_write)
            print("DONE WITH IMAGE WRITE")

            #----------------------->>>>>>>>>>>>>>>>>>>> img path for testing
            # captured_img_pth1 = "D:\images\img_637b13e7b8d1506af014e04f.jpg"
            # captured_img_pth1 = img_path
            #_--------------------------------------->>>>>>>>>>>>>>


            # time_taken_in_image_captur=time.time()-start_time_check_bottom1
            # print("TIME TAKEN IN IMAGE TAKEN AND WRITING ON DISK IS *****************************",time_taken_in_image_captur)   
            start_time_for_pyzbar=time.time()
            

            eu_number=barcode_scanner(captured_img_pth1)
            
            time_taken=start_time_for_pyzbar-time.time()
            print("TIME TAKEN IN PYZBAR $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",time_taken)
            # print(eu_number)
            if  eu_number:
                print("eu is            ----------------------",eu_number)
                # eu_number = eu_number.replace(" ","")
                mp_1=MongoHelper().getCollection("master_file")
                # mp_2 =MongoHelper().getCollection("parts")
                # doc = []
                for p in eu_number:
                    p = p.replace(" ","")
                    print('ppppp',p)
                    doc =  mp_1.find_one({'EAN':str(p)})
                    if doc is not None:
                        eu_number=str(p)
                        break
                    # print(doc)
                    # doc.append(doc1)
                # print("DOc9999999999999999999999999999",doc[0])
                # if len(doc)>1:
                #     if doc[0] is None:
                #         doc = doc[0]
                #     else:
                #         doc = doc[1]
                # else:
                #     doc =doc[0]
                # doc =doc[0]
                if doc is None:
                    res={}
                    message="NO RECORD FOUND FOR THIS EAN"
                    status1={"isvalid":False}
                    status=400
                    return res,status1,message,status 

                   
                      
                else:
                    model_num =  doc['Material']
                    amount=doc['Amount']
                    country_db=doc['Country of Origin']
                    description=doc["Material description"]
                    # nextstep = True
                    if model_num=='' or amount=='' or country_db=='' or description=='':
                        print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                        res={}
                        message="Complete information to print a label not availabe"
                        status=400
                        status1={"isvalid":False}
                        return res,status1,message,status 

                    
                start_time=time.time()    
                stat_,final_value,date_list,year_format=ocr_status_details(captured_img_pth1,country_db)
                print("result from ocr is %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",date_list)
                # print("result from ocr is %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",len(date_list))
                time_for_paddle_ocr=time.time()-start_time
                print("Time Taken FOR PADDLE OCR IS ",time_for_paddle_ocr)
                if final_value is None:
                    print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                    res={}
                    message="UNABLE TO FIND FORMAT FROM MASTER FILE"
                    status=400
                    status1={"isvalid":False}
                    return res,status1,message,status 

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
                    message="No Country available"
                    status=400
                    status1={"isvalid":False}
                    return res,status1,message,status 
                elif len(date_list)==0:
                    print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                    res={}
                    message="No Country available"
                    status=400
                    status1={"isvalid":False}
                    return res,status1,message,status     


                else:

                        
                    print("<<<<<<<<<<<<<<<date list<<<<<<<",date_list)
                    if len(date_list[-2]) == 2:
                        date_year=str(20)+date_list[-2] 
                    else:
                        date_year = str(date_list[-2])
                    date_week=date_list[-1]
                    month,year=getMonth(int(date_year),int(date_week))
                    print("month is ]]]]]]]]]]]]]]]]",month)
                    mfg_date=month+"/"+date_year
                    image_url='http://localhost:3306/'+image_name
                    mp.update_one({'_id':ObjectId(_inspection_id)}, {"$set": { "Model_number":model_num,"Manufacturing_date":mfg_date,"Copies":1,"Quantities":1,"EU13":eu_number,'Amount':amount ,"country":country_db,"status":stat_,"image_url":image_url,"description":description,"user_name":user_name,"year_format":year_format,"actual_raw_date":final_value}},upsert=True)
                    mp2=MongoHelper().getCollection("Current_inspection")
                    mp2.update_one({'_id':ObjectId(iid)}, {"$set": { "Model_number":model_num,"Manufacturing_date":mfg_date,"Copies":1,"Quantities":1,"EU13":eu_number,'Amount':amount ,"country":country_db,"status":stat_,"image_url":image_url,"state":"started","actual_raw_date":final_value}},upsert=True)

                    res={ "model_number":model_num,"mfg_date":mfg_date ,"eu_number":eu_number,"image_url":image_url,"inspection_id":_inspection_id,"image_url":image_url,"status":stat_,"copies":1,"qunatity":1,"actual_raw_date":final_value}
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
          

    
        

                    











def date_maker(date,country_format):
    ### TH2240
    ### THialand
    ### country-format
     
            
    fin = date
    year=country_format
    # print('zzzzzzzzzzzzzzzzzzz4zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',final_val)
    date_list = []
    # for fin in final_val:
    #     for year in year_code:
    if len(year) == len(fin):
        if "MONTH" in year:
            work_year = year[2:-1]
            work_month = year[:3]
            # date_list.append(work_year)
            # date_list.append(work_month)
            # print(">>>>>>>>>>>>>>>>>>>>>>",year)

        elif 'WX' in fin:
                            # print('coronaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            target_y = "Y"
            start_position_Y = year.index("Y")
            last_pos_Y = len(year) - 1 - year[::-1].index(target_y)
            work_year = fin[start_position_Y:last_pos_Y+1]

            target_w = "W"
            last_pos_w = len(year) - 1 - year[::-1].index(target_w)
            work_week = fin[last_pos_w+1:last_pos_w+3]    
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
        if len(date_list[-2]) == 2:
            date_year=str(20)+date_list[-2] 
        else:
            date_year = str(date_list[-2])
        date_week=date_list[-1]
        month=getMonth(int(date_year),int(date_week))
        if int(date_week)>53:
            return None
        if month is 0 :

            return None    
        else:

            print("month is ]]]]]]]]]]]]]]]]",month)
            mfg_date=month+"/"+date_year
            print("date list id 8888888888888888*****************************",date_list)
            # date_l=[]
        # date_l.append()
        # date_list

            # return final_val,date_list
            return mfg_date
def date_maker_by_date(country_db,date):
    date = date.replace(" ","")
    mp_country = MongoHelper().getCollection("country_code")

    country_list = [i for i in mp_country.find({'Country of origin':country_db})]
    print('>>>>>>>>>>>>>>>>',date)
    print('>>>>>>>>>>>>>>>>country list',country_list)


    country_code = set()
    len_date_format = []
    year_code = []
    for i in country_list:
        date_format = (i['Maufacturing date code format']).replace(" ","")
        len_date_format.append(len(date_format))
        country_code.add((i['Maufacturing date code format']).replace(" ","")[:2])
        year_code.append((i['Maufacturing date code format']).replace(" ",""))
        print(len_date_format)
    print('>>>>>>>>>>>>>>>yererarrasss>>>',year_code)
    further_val  = []
    print("your tttttttttttttttt^^^^^^^^^^^^^^^^^",len_date_format)
    for l in len_date_format:
        if (l) == len(date):
            further_val.append(date)

    print('&&&&&&&&&&&&&&&&&&&&&&&&99999999999999999999((((((((((((()))))))))))))))))',further_val)
    final_val = set()
    for fthr_val in further_val:
        for cnt_code in country_code:
            if cnt_code == fthr_val[:2]:
                final_val.add(fthr_val)
    
            
    final_val = list(final_val)
    print('zzzzzzzzzzzzzzzzzzz4zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzfianl vake rrzzzzz',final_val)
    date_list = []
    for fin in final_val:
        for year in year_code:
            # print()
            if len(year) == len(fin):
                year_format = year
                # print('yearrrrrrrrrrrrrrrrcodeeeeeeeeeeeeeee',year)
                if "MONTH" in year:
                
                    work_year = year[2:-1]
                    work_month = year[:3]
                    # date_list.append(work_year)
                    # date_list.append(work_month)
                    # print(">>>>>>>>>>>>>>>>>>>>>>",year)
                #     # print("<<<<<<<<<<<<<<<<<<<<<<",fin)
                # elif country_db.lower() == 'china' and 'WX' in fin:
                #             # print('coronaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                #             target_y = "Y"
                #             start_position_Y = year.index("Y")
                #             last_pos_Y = len(year) - 1 - year[::-1].index(target_y)
                #             work_year = fin[start_position_Y:last_pos_Y+1]

                #             target_w = "W"
                #             last_pos_w = len(year) - 1 - year[::-1].index(target_w)
                #             work_week = fin[last_pos_w+1:last_pos_w+3]    
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
    # print("date list id 8888888888888888*****************************",date_list)
    # date_l=[]
    # date_l.append()
    # print('????????????????????????????????',year)

    # final_val=final_val[0]
    # print("year frrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",year_format)
    return date_list[0:2]
    #except Exception as e:
    # return None
    
def manual_entry_utils(data):
    
    # if edited["EU13"]!="":
    # print("NO EDITED VALUE")
    eu_13=data.get("eu_number")
    label_type=data.get("label_type",None)
    actual_mfg_date=data.get("actual_mfg_date")
    quanatity=data.get('quantities')
    copies=data.get('copies')
    inspection_id=data.get("inspection_id",None)
    user=data.get("user")
    user_name=user["username"]
    font_size=data.get("font_size")
    print_des={"font_size":font_size,
                    "label_type":label_type}
    if inspection_id is not None:
        createdAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        createDate = datetime.now().strftime("%d-%m-%Y")
        COLL_NAME = "INSPECTION_"+datetime.now().strftime("%m_%y")
        mp = MongoHelper().getCollection("inspection_"+str(inspection_id))
        mp2=MongoHelper().getCollection("Current_inspection")
        mp = MongoHelper().getCollection("inspection_"+str(inspection_id))
        obj={
                    'start_time':createdAt,
                    'created_date':createDate,
                    "font_size":font_size,
                    "label_type":label_type

                }
        _inspection_id=mp.insert_one(obj).inserted_id
    
        print("hey eu is ",eu_13)
    edited={}
    act={}
    if  eu_13:
        print("eu is            ----------------------",eu_13)
        eu_number = eu_13.replace(" ","")
        mp_1=MongoHelper().getCollection("master_file")
        # mp_2 =MongoHelper().getCollection("parts")
        doc =  mp_1.find_one({'EAN':str(eu_number)})
        # print("DOc9999999999999999999999999999",doc)
        if doc is None:
            preview={}
            act={}
            edited={}
            message="NO RECORD FOUND FOR THIS EAN"
            status1={"isvalid":False}
            status=400
            # return res,status1,message,status 
            return act,edited,preview,message,status1,status,label_type,font_size

            
        else:
            edited['Model_number'] =  doc['Material']
            model_number=doc["Material"]
            edited["Quantities"]=quanatity
            edited["Copies"]=copies

            edited['Amount']  =doc['Amount']
            amount_=doc["Amount"]
            country_db=doc['Country of Origin']
            description=doc["Material description"]
            edited["actual_raw_date"]=actual_mfg_date
        
            prdeict_dt=date_maker_by_date(country_db,actual_mfg_date)
            # if len(prdeict_dt)
            # edited["actual_raw_date"]=prdeict_dt
            print("HEY DATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT,8888888888888888888888",prdeict_dt)
            if len(prdeict_dt)==2:
                print("newdater ",prdeict_dt[-1])
                if int(prdeict_dt[-1])>53:
                    print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                    res={}
                    message="Wrong week or  month no Such date exist"
                    status=400
                    status1={"isvalid":False}
                    return act,edited,res,message,status1,status,label_type,font_size

                elif len(prdeict_dt[-2]) == 2:
                    print("yessssssssssssssssssssssssssssssssssss")
                    date_year=str(20)+prdeict_dt[-2] 
                else:
                    print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
                    date_year = str(prdeict_dt[-2])
                date_week=prdeict_dt[-1]
                act={}
                # date_year = str(20)+str(prdeict_dt[-2])
                date_week=prdeict_dt[-1]
                print("date year is ssssssssssssssssssssssssssssss00000000000000000000000000000000",date_year)
                month=getMonth(int(date_year),int(date_week))
                if month==0:
                    print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                    res={}
                    message="DATE YEAR MORE THAN CURRENT YEAR"
                    status=400
                    status1={"isvalid":False}
                    return act,edited,res,message,status1,status,label_type,font_size
                else:    
                    print("month is ]]]]]]]]]]]]]]]]",month)
                    mfg_date=month+"/"+
                    
                    
                    print("data come s",mfg_date)
                    edited["Manufacturing_date"]=mfg_date
                    
                    amount_= float(amount_)*float(quanatity)
                    print(amount_)
                    edited['EU13']=eu_13
                    # print("AMOU N T IS ",edited["Amount"])
                    # act=edited
                    mp.update_one({'_id':ObjectId(_inspection_id)}, {"$set": { "isEdited":True, "Model_number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_number,'Amount':amount_ ,"country":country_db,"status":"Accepted","description":description,"user_name":user_name,"actual":act,"edited":edited}},upsert=True)
                    preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
                    mp2=MongoHelper().getCollection("Current_inspection")
                    if mp2 is not None:
                        coll=[ i for i in mp2.find()]
                        coll=coll[-1]

                        id_=coll["_id"]

                        mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}})
                    
                    message="Success"
                    status1={"isvalid":True}
                    return act,edited,preview,message,status1,200,label_type ,font_size
                
            if prdeict_dt is None:
                print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                res={}
                message="No Country available with such format"
                status=400
                status1={"isvalid":False}
                return act,edited,res,message,status1,status,label_type,font_size
            elif len(prdeict_dt)==1:
                print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                res={}
                message="No Country available with such format"
                status=400
                status1={"isvalid":False}
                return act,edited,res,message,status1,status,label_type,font_size

                # return res,status1,message,status 
            elif len(prdeict_dt)==0:
                print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                res={}
                message="No Country available with such format"
                status=400
                status1={"isvalid":False}
                # return res,status1,message,statu
                return act,edited,res,message,status1,status,label_type,font_size
                    

  
def submit_process_util(data):
    # try:
        l=[]
        model_number=data.get("model_number",None).upper()
        print("mOdel_number",model_number)
        eu_13=data.get("eu_number",None)
        print("eu_13 is ",eu_13)

        mfg_date=data.get("mfg_date",None)
        print("mfg is ",mfg_date)
        # year_format="THYYWW"
        # mfg_date=date_maker(mfg_date,year_format)
        # print("HEY BRO MFG IS ",mfg_date)


        quanatity=data.get("quantities",None)
        print("qudsjdb is ",quanatity)

        copies=data.get("copies",None)
        print("copies is ",copies)
        actual_raw_date=data.get("actual_raw_date")
        


        
        # amount=int(quanatity)*int(copies)
        _id=data.get("inspection_id",None)
        print("id is ",_id)
        # description=data.get("description")

       
        
            
        
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
            year_format=ins["year_format"]
            amount=ins['Amount']
            country_db=ins["country"]
            act["actual_raw_date"]=ins["actual_raw_date"]
            label_type=ins['label_type']
            font_size=["font_size"]
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
            
            country_db=ins["country"]
            __id=ins["_id"]
            year_format=ins["year_format"]
            act["actual_raw_date"]=ins["actual_raw_date"]
            label_type=ins['label_type']
            font_size=["font_size"]



            
            
        print("ACTUAL DATA IS %%%%%%%%%%%%^^^^^^^^^^^^^^^^^^^",edited)
        # print("sgdjasdgfjhsdagffffffffffffjasd",insp_coll)
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
        if (act['actual_raw_date'])==actual_raw_date:
            edited['actual_raw_date']=""
        else:
            edited['actual_raw_date']=actual_raw_date    
        print("EDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDITED",edited)
       
        print("EA NUMBER IS ",edited["EU13"])
        ### if user edit only actual date so  we will convert date in same way
        if edited['Model_number']=="" and edited['EU13']=="" and edited["actual_raw_date"]=="" and edited["Copies"]=="" and edited["Quantities"]=="":
           

               

            amount_=amount
            amount_= float(amount_)*float(quanatity)
            print(amount_)
            # edited['Amount']=amount_        # print("AMOU N T IS ",edited["Amount"])
                    
            mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}},upsert=True)
            preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
            mp2=MongoHelper().getCollection("Current_inspection")
            if mp2 is not None:
                coll=[ i for i in mp2.find()]
                coll=coll[-1]
                id_=coll["_id"]

                mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}})
            print("goING IN FIRST CONDITION ")
            message="Success"
            status1={"isvalid":True}
            return act,edited,preview,message,status1,200,label_type,font_size

        elif edited['Model_number']=="" and edited['EU13']=="" and edited["actual_raw_date"]=="" and edited["Copies"]=="" and edited["Quantities"]!="":
        

            print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")

            amount_=amount
            amount_= float(amount_)*float(quanatity)
            print(amount_)
            edited['Amount']=amount_        # print("AMOU N T IS ",edited["Amount"])
                    
            mp.update_one({'_id':ObjectId(__id)}, {"$set": { "isEdited":True,"actual":act,"edited":edited}},upsert=True)
            preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
            mp2=MongoHelper().getCollection("Current_inspection")
            if mp2 is not None:
                coll=[ i for i in mp2.find()]
                coll=coll[-1]
                id_=coll["_id"]

                mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}})
            print("goING IN FIRST CONDITION ")
            message="Success"
            status1={"isvalid":True}
            return act,edited,preview,message,status1,200,label_type,font_size



        elif edited['Model_number']=="" and edited['EU13']=="" and edited["actual_raw_date"]=="" and edited["Copies"]!="" and edited["Quantities"]=='':
           
            print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
               

            amount_=amount
            amount_= float(amount_)*float(quanatity)
            print(amount_)
            # edited['Amount']=amount_        # print("AMOU N T IS ",edited["Amount"])
                    
            mp.update_one({'_id':ObjectId(__id)}, {"$set": {  "isEdited":True,"actual":act,"edited":edited}},upsert=True)
            preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
            mp2=MongoHelper().getCollection("Current_inspection")
            if mp2 is not None:
                coll=[ i for i in mp2.find()]
                coll=coll[-1]
                id_=coll["_id"]

                mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}})
            print("goING IN FIRST CONDITION ")
            message="Success"
            status1={"isvalid":True}
            return act,edited,preview,message,status1,200,label_type,font_size

        elif edited['Model_number']=="" and edited['EU13']=="" and edited["actual_raw_date"]=="" and edited["Copies"]!="" and edited["Quantities"]!='':
           
            print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
               

            amount_=amount
            amount_= float(amount_)*float(quanatity)
            edited["Amount"]=amount_
            print(amount_)
            # edited['Amount']=amount_        # print("AMOU N T IS ",edited["Amount"])
                    
            mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}},upsert=True)
            preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
            mp2=MongoHelper().getCollection("Current_inspection")
            if mp2 is not None:
                coll=[ i for i in mp2.find()]
                coll=coll[-1]
                id_=coll["_id"]

                mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "isEdited":True, "actual":act,"edited":edited}})
            print("goING IN FIRST CONDITION ")
            message="Success"
            status1={"isvalid":True}
            return act,edited,preview,message,status1,200,label_type,font_size
        
        elif edited['Model_number']=="" and edited['EU13']=="" and edited["actual_raw_date"]!="" and edited["Copies"]!="" and edited["Quantities"]!='':
           
            print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
               

            amount_=amount
            amount_= float(amount_)*float(quanatity)
            edited["Amount"]=amount_
            print(amount_)
            # edited['Amount']=amount_        # print("AMOU N T IS ",edited["Amount"])
                    
            mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}},upsert=True)
            preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
            mp2=MongoHelper().getCollection("Current_inspection")
            if mp2 is not None:
                coll=[ i for i in mp2.find()]
                coll=coll[-1]
                id_=coll["_id"]

                mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "isEdited":True, "actual":act,"edited":edited}})
            print("goING IN FIRST CONDITION ")
            message="Success"
            status1={"isvalid":True}
            return act,edited,preview,message,status1,200,label_type,font_size  
        
        elif edited['Model_number']=="" and edited['EU13']=="" and edited["actual_raw_date"]!=""  and edited["Quantities"]!='':
           
            print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
               

            amount_=amount
            amount_= float(amount_)*float(quanatity)
            edited["Amount"]=amount_
            print(amount_)
            # edited['Amount']=amount_        # print("AMOU N T IS ",edited["Amount"])
                    
            mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}},upsert=True)
            preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
            mp2=MongoHelper().getCollection("Current_inspection")
            if mp2 is not None:
                coll=[ i for i in mp2.find()]
                coll=coll[-1]
                id_=coll["_id"]

                mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "isEdited":True, "actual":act,"edited":edited}})
            print("goING IN FIRST CONDITION ")
            message="Success"
            status1={"isvalid":True}
            return act,edited,preview,message,status1,200,label_type,font_size      

        if edited['Model_number']=="" and edited['EU13']=="" and edited["actual_raw_date"]!="":
            mfg_date=date_maker(actual_raw_date,year_format)
            print("MFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG*******************",mfg_date)
            if mfg_date is None:
                preview={}
                message="WRONG DATE FORMAT OR VALUE"
                status1={"isvalid":False}
                status=400
                # return res,status1,message,status 
                return act,edited,preview,message,status1,status,label_type,font_size
            else:

                edited['Manufacturing_date']=mfg_date

                amount_=amount
                amount_= float(amount_)*float(quanatity)
                print(amount_)
                        # print("AMOU N T IS ",edited["Amount"])
                        
                mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}},upsert=True)
                preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
                mp2=MongoHelper().getCollection("Current_inspection")
                if mp2 is not None:
                    coll=[ i for i in mp2.find()]
                    coll=coll[-1]
                    id_=coll["_id"]

                    mp2.update_one({'_id':ObjectId(id_)}, {"$set": {  "isEdited":True,"actual":act,"edited":edited}})
                print("goING IN FIRST CONDITION ")
                message="Success"
                status1={"isvalid":True}
                return act,edited,preview,message,status1,200,label_type,font_size
    
        
        
        ### if user edit MODEL NUMBER OR EU nUMBER   so  we will convert date in same way

        else:
            if edited["EU13"]!="":
                print("NO EDITED VALUE")
                eu_13=edited["EU13"]
                print("hey eu is ",eu_13)
                if  eu_13:
                    print("eu is            ----------------------",eu_13)
                    eu_number = eu_13.replace(" ","")
                    mp_1=MongoHelper().getCollection("master_file")
                    # mp_2 =MongoHelper().getCollection("parts")
                    doc =  mp_1.find_one({'EAN':str(eu_number)})
                    # print("DOc9999999999999999999999999999",doc)
                    if doc is None:
                        preview={}
                        message="NO RECORD FOUND FOR THIS EAN"
                        status1={"isvalid":False}
                        status=400
                        # return res,status1,message,status 
                        return act,edited,preview,message,status1,status,label_type,font_size
    
                        
                    else:
                        edited['Model_number'] =  doc['Material']
                        edited['Amount']  =doc['Amount']
                        amount_=doc["Amount"]
                        country_db=doc['Country of Origin']
                        description=doc["Material description"]
                    
                        prdeict_dt=date_maker_by_date(country_db,actual_raw_date)
                        # if len(prdeict_dt)
                        # edited["actual_raw_date"]=prdeict_dt
                        print("HEY DATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",prdeict_dt)
                        if len(prdeict_dt)==2:

                            date_year = str(20)+str(prdeict_dt[-2])
                            date_week=prdeict_dt[-1]
                            if int(date_week)<53:

                                month=getMonth(int(date_year),int(date_week))
                                print("month is ]]]]]]]]]]]]]]]]",month)
                                mfg_date=month+"/"+date_year
                                print("data come s",mfg_date)
                                edited["Manufacturing_date"]=mfg_date
                                
                                amount_= float(amount_)*float(quanatity)
                                print(amount_)
                                # print("AMOU N T IS ",edited["Amount"])
                                
                                mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}},upsert=True)
                                preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
                                mp2=MongoHelper().getCollection("Current_inspection")
                                if mp2 is not None:
                                    coll=[ i for i in mp2.find()]                                
                                    coll=coll[-1]
                                    id_=coll["_id"]

                                    mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "isEdited":True, "actual":act,"edited":edited}})
                                
                                message="Success"
                                status1={"isvalid":True}
                                return act,edited,preview,message,status1,200,label_type,font_size  
                            elif int(date_week)>53:
                                print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                                res={}
                                message="No Country available with such format"
                                status=400
                                status1={"isvalid":False}
                                return act,edited,res,message,status1,status,label_type,font_size

                        if prdeict_dt is None:
                            print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                            res={}
                            message="No Country available with such format"
                            status=400
                            status1={"isvalid":False}
                            return act,edited,res,message,status1,status,label_type,font_size
                        elif len(prdeict_dt)==1:
                            print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                            res={}
                            message="No Country available with such format"
                            status=400
                            status1={"isvalid":False}
                            return act,edited,res,message,status1,status,label_type,font_size

                            # return res,status1,message,status 
                        elif len(prdeict_dt)==0:
                            print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                            res={}
                            message="No Country available with such format"
                            status=400
                            status1={"isvalid":False}
                            # return res,status1,message,statu
                            return act,edited,res,message,status1,status,label_type,font_size
                    
            if edited["Model_number"]!="":
                print("NO EDITED VALUE")
                Model_number=edited["Model_number"]
                print("hey eu is ",Model_number)
                if  eu_13:
                    print("eu is            ----------------------",Model_number)
                    Model_number = Model_number.replace(" ","")
                    mp_1=MongoHelper().getCollection("master_file")
                    # mp_2 =MongoHelper().getCollection("parts")
                    doc =  mp_1.find_one({'Material':str(Model_number)})
                    # print("DOc9999999999999999999999999999",doc)
                    if doc is None:
                        preview={}
                        message="NO RECORD FOUND FOR THIS MODEL NUMBER"
                        status1={"isvalid":False}
                        status=400
                        # return res,status1,message,status 
                        return act,edited,preview,message,status1,status,label_type,font_size
    
                        
                    else:
                        edited['EU13'] =  doc['EAN']
                        edited['Amount']  =doc['Amount']
                        amount_=doc["Amount"]
                        country_db=doc['Country of Origin']
                        description=doc["Material description"]
                    
                        prdeict_dt=date_maker_by_date(country_db,actual_raw_date)
                        # if len(prdeict_dt)
                        # edited["actual_raw_date"]=prdeict_dt
                        print("HEY DATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",prdeict_dt)
                        if len(prdeict_dt)==2:
                            if int(date_week)>53:
                                print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                                res={}
                                message="No Country available with such format"
                                status=400
                                status1={"isvalid":False}
                                return act,edited,res,message,status1,status,label_type,font_size
                            elif int(date_week) <53:
                                    
                                date_year = str(20)+str(prdeict_dt[-2])
                                date_week=prdeict_dt[-1]
                                month=getMonth(int(date_year),int(date_week))
                                print("month is ]]]]]]]]]]]]]]]]",month)
                                mfg_date=month+"/"+date_year
                                print("data come s",mfg_date)
                                edited["Manufacturing_date"]=mfg_date
                                
                                amount_= float(amount_)*float(quanatity)
                                print(amount_)
                                # print("AMOU N T IS ",edited["Amount"])
                                
                                mp.update_one({'_id':ObjectId(__id)}, {"$set": { "actual":act,"edited":edited,"Copies":edited["Copies"],"Quantities":edited["Quantities"]}},upsert=True)
                                preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
                                mp2=MongoHelper().getCollection("Current_inspection")
                                if mp2 is not None:
                                    coll=[ i for i in mp2.find()]                                
                                    coll=coll[-1]
                                    id_=coll["_id"]

                                    mp2.update_one({'_id':ObjectId(id_)}, {"$set": { "isEdited":True, "actual":act,"edited":edited}})
                            
                                message="Success"
                                status1={"isvalid":True}
                                return act,edited,preview,message,status1,200,label_type,font_size
                            
                        if prdeict_dt is None:
                            print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                            res={}
                            message="No Country available with such format"
                            status=400
                            status1={"isvalid":False}
                            return act,edited,res,message,status1,status,label_type,font_size
                        elif len(prdeict_dt)==1:
                            print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                            res={}
                            message="No Country available with such format"
                            status=400
                            status1={"isvalid":False}
                            return act,edited,res,message,status1,status,label_type,font_size

                            # return res,status1,message,status 
                        elif len(prdeict_dt)==0:
                            print("Nothing ^^^^^^^^^^^^^^^^^^^^^")
                            res={}
                            message="No Country available with such format"
                            status=400
                            status1={"isvalid":False}
                            # return res,status1,message,statu
                            return act,edited,res,message,status1,status,label_type,font_size
            # else:
            #     act={1:1}
            #     edited={1:1}
            #     preview={2:2}

            #     act=[],edited=[],preview=[],401

        # except Exception as e:
        #     return e , 400


def print_inspection(data):
    l=[]
    amount=data.get("Amount")
    print("data coming from frontend for printing     *88***************************************",amount)
    
    country=data.get("Country")
    description=data.get("description")
    
    createdAt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    createDate = datetime.now().strftime("%Y-%m-%d")
    label_type=data.get("label_type")
    font_size=data.get("font_size")
    model_number=data.get("Model_Number")

    mfg_date=data.get("Manufacturing_date")
    quanatity=data.get("Quantities")
    copies=data.get("Copies")
    if label_type=="MRP" and font_size=="1mm":
        directory="D:/PRINT_TEXT_FILES/MRP_1_mm/"
    elif label_type=="MRP" and font_size=="2mm":
        directory="D:/PRINT_TEXT_FILES/MRP_2_mm/"    
    elif label_type=="WHOLESALE" and font_size=="1mm":
        directory="D:/PRINT_TEXT_FILES/WHOLESALE_1_mm/" 
        # D:\PRINT_TEXT_FILES\WHOLESALE _1_mm 
    elif label_type=="WHOLESALE" and font_size=="2mm":
        directory="D:/PRINT_TEXT_FILES/WHOLESALE_2_mm/"        

    
    l.extend(["Date;MRP;Origin;Model;Qty;Copy;description" '\n',str(mfg_date)+";"+str(amount)+";"+str(country)+";"+str(model_number)+";"+str(quanatity)+";"+str(copies)+";"+str(description)])
    file1 = open(directory+str(createdAt)+".txt","w")
    file1.writelines(l)
    file1.close()
    mp2=MongoHelper().getCollection("Current_inspection")

    if mp2 is not None:
        coll=[i for i in mp2.find()]
        coll=coll[-1]
        id_=coll["_id"]
        print("id is )))))))))))))))((((((((((((((((((((((((((((((",id_)
        mp2.update_one({'_id':ObjectId(id_)}, {"$set": {"state": "completed"}})
    # mp=MongoHelper().getCollection("Current_inspection")
    # mp.update_one({'_id':ObjectId(inspection_id)}, {"$set": {"status": "completed"}})
    return 200





    

def end_process_util(data):
    #from datetime import datetime
    inspection_id  = data.get('inspection_id', None)

    
    mp = MongoHelper().getCollection("inspection")
    
 
    mp.update_one({'_id':ObjectId(inspection_id)}, {"$set": {"status": "completed"}})
    # preview={ "Model_Number":model_number,"Manufacturing_date":mfg_date,"Copies":copies,"Quantities":quanatity,"EU13":eu_13,"Amount":str(amount_),"Country":country_db,"description":description}
    mp2=MongoHelper().getCollection("Current_inspection")

    if mp2 is not None:
        coll=[i for i in mp2.find()]
        coll=coll[-1]
        id_=coll["_id"]
        print("id is )))))))))))))))((((((((((((((((((((((((((((((",id_)
        mp2.update_one({'_id':ObjectId(id_)}, {"$set": {"state": "completed"}})

    else:
        coll=[i for i in mp2.find()]
        coll=coll[-1]
        id_=coll["_id"]
        print("id is )))))))))))))))((((((((((((((((((((((((((((((",id_)

        mp2.update_one({'_id':ObjectId(id_)}, {"$set": {"state": "completed"}})


    return "Success",200

def update_file_details(data):
    # try:
        mp = MongoHelper().getCollection('master_file')
        mp1 = MongoHelper().getCollection('mini_master')
        import json
        # request.POST.get
        user=data.POST.get("user")
        user=json.loads(user)
        user_name=user["username"]        
        # user_name="Operator1"
        insp_coll = [i for i in mp.find()]
        file = data.FILES.get('file')
        
        df = pd.read_excel(file,'SEIPL',engine='openpyxl',converters={'EAN':str,'Amount':str})
        print("YES  ALL DONE----------------------------------------",df)
        if 'EAN' not in df:
            print("NO EAN FOUND")
        if 'Material' not in df:
            print("Material ")   
        if 'Material Description' not in df:
            print("Material description ") 
        if 'Amount' not in df:
            print("Amount ")
        if 'Unit' not in df:
            print("Amount 'Unit ")
        if 'UoM' not in df:
            print("Amount UoMM ")
        if 'Country of Origin' not in df:
            print("'Country of Origin ")        
        if ('EAN' not  in df) or ('Material' not  in df) or ('Material Description' not  in df) or ('Amount' not  in df) or ('Unit' not  in df )or ('UoM' not  in df ) or ('Country of origin' not  in df):  
            message = 'Wrong sheet or  Required column not available'
            print("insiddd")
            return message , 200         
        if 'EAN' and 'Material'and 'Material Description'and 'Amount' and 'Unit' and 'UoM' and 'Country of origin' in df:
            print("YES  ALL DONE")
            df1 = df[['EAN','Material','Material Description','Amount','Unit','UoM','Country of origin']]
            df1['C'] =(np.arange(len(df1)))
            df1=df1.applymap(str)
            df1["Uploaded By"]=user_name
            df1["Upload Date"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            dist =df1.set_index((df1['C'])).T.to_dict()
            # df2 = pd.DataFrame(df1['EAN'].apply(str))
            # # df2['eu-number'] = 
            # dist =df1.set_index(df2['EAN']).T.to_dict()
            valuesList = list(dist.values())
            # mp.insert_one(user_name)

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
            return message , 200
        else:
            message = 'Wrong sheet/ Required column not available'
        return message , 400
    # except Exception as e:
    #     return e , 400

    

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
def get_dateformat_file_details(data):

    try:
        mp = MongoHelper().getCollection('country_code')
        part_list = [i for i in mp.find()]
        if len(part_list)==0:
            part_list=[]
            return part_list,200
        else:

            return part_list , 200
    except Exception as e:
        print(e)

@singleton
def test():
    # try:
    import neoapi
   
    try:
             
        camera_ip_bottom_thr3 = "192.168.1.2"
        camera_bottom_thr3 = neoapi.Cam() #site
        print(camera_bottom_thr3.Connect(camera_ip_bottom_thr3))
        print("connected")
        res =  True
    # imgarray_bottom_three = camera_bottom_thr3.GetImage().GetNPArray()
    # except (NoAccessException):
    #     res = True
    except neoapi.neoapi.NoAccessException:
        print('8888888888888888888888888888888888888888')
        res =True
    except neoapi.neoapi.NotConnectedException:
        print('hereeeeeeeeeeeeeeeeeeeeeeeeee')
        res =False
 

    # except Exception as e:
    #     print('>>>>>>>>>>>>>>>>>>>')
    #     print(type(e))
    #     print([e])
    #     if e == neoapi.neoapi.NotConnectedException:
    #         res =False
    #     else:
    #         res = True
    # print("RESYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",res)    
    return res


def health_check_details(data):
    rch=CacheHelper()
    # try:
    result={}
    feed = False
    
    start_time_check_bottom1 = time.time()
    rch.set_json({'camera_original':None})
    rch.set_json({'camera_trigger':True})
    while True:
        # time.sleep(1.5)
        bottom_one_write = rch.get_json('camera_original')
        if bottom_one_write is not None:
            print("got it ")
            feed=True
            # rch.set_json({cam_health:})
            rch.set_json({'camera_original':None})
            break
        if time.time() - start_time_check_bottom1 > 5:
            break 
        
       
    result['camera'] = feed
        
            
    return result , 200

            # start_time_check_bottom1 = time.time()
            # rch.set_json({'camera_original':None})
            # rch.set_json({'camera_trigger':True})
            # while True:
            #     # time.sleep(1.5)
            #     bottom_one_write = rch.get_json('camera_original')
            #     if bottom_one_write is not None:
            #         feed=True
            #         # rch.set_json({cam_health:})
            #         rch.set_json({'camera_original':None})
            #         break
            #     if time.time() - start_time_check_bottom1 > 5:
            #         break   


        # while True:
        #         # time.sleep(1.5)
        #         bottom_one_write = rch.get_json('camera_original')
        #         if bottom_one_write is not None:
        #             print('Read the image')
        #             # rch.set_json({cam_health:})
        #             rch.set_json({'camera_original':None})
        #             break
        #         if time.time() - start_time_check_bottom1 > 20:
        #             break
        
    # except Exception as e:
    #     print(e)


