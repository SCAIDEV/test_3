"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
# from PIL import Image
import cv2
# import torch
from flask import Flask, request
# import base64
from io import BytesIO
import time
import json
from flask import jsonify
from mongohelper import MongoHelper
# from base64 import decodestring
from paddleocr import PaddleOCR
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
app = Flask(__name__)

DETECTION_URL = "/ocr"


@app.route(DETECTION_URL, methods=["POST"])
def predict():

    if request.method == "POST":

        data = request.get_json(silent=False)

        orig_base64 = data['original_image']
        mp_country = MongoHelper().getCollection("country_code")
    #try:
        m=time.time()
        #ocr = PaddleOCR(lang='en',use_gpu=True)
        # img_path ="D:\images\img_6368b67a2e7f89bb029bbd4f.jpg"
        # regions = regions
        # frame =cv2.imread(img_path)
        # print("SIZE OF FRAME : : : : : : : : : : : : : : : : :",frame.shape)
        # # frame = cv2.resize(frame,(640,480))
        result = result = ocr.ocr(orig_base64, cls=True)
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",result)
        end_time=time.time()
        
        # result = ocr.ocr(img_path,cls=False)
        print("Time taken for model loading and infrencing is ",end_time-m)
        # from re import search
        val  = "made"
        prediction = []
        country_found=0
        for line in result:
            for j in line:
                
                prediction.append(j[-1][0].replace(" ",""))
                if val in j[-1][0].lower():
                    country_found=1
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
        # print('<,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,HHHH',country)
        # country="Thailand"
        # print("Country is <<<<<<<<<<<<",country)
        # if country_found==1:

            country_list = [i for i in mp_country.find({'Country of origin':country})]
            print('>>>>>>>>>>>>>>>>>>>>>>>>hhhhhhhhhhhhhhhhhhhhhhh>>>>>',country_list)
            country_code = set()
            len_date_format = []
            year_code = []
            for i in country_list:
                date_format = (i['Maufacturing date code format']).replace(" ","")
                len_date_format.append(len(date_format))
                country_code.add((i['Maufacturing date code format']).replace(" ","")[:2])
                year_code.append((i['Maufacturing date code format']).replace(" ",""))
                # print(len_date_format)
            # print('>>>>>>>>>>>>>>>>>>',year_code)
            further_val  = []
            print('??????????????????????????',prediction)
            print('????????????????????????????',len_date_format)
            for pred in prediction:
                for l in len_date_format:
                    if l == len(pred):
                        further_val.append(pred)

            # print('&&&&&&&&&&&&&&&&&&&&&&&&',further_val)
            final_val = set()
            for fthr_val in further_val:
                for cnt_code in country_code:
                    if cnt_code == fthr_val[:2]:
                        final_val.add(fthr_val)
            
                    
            final_val = list(final_val)
            # print('zzzzzzzzzzzzzzzzzzz4zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',final_val)
            date_list = []
            for fin in final_val:
                for year in year_code:
                    if len(year) == len(fin):
                        if "MONTH" in year:
                            # print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
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
            # else:
            #     date_list=[]
            #     return date_list
        
        return jsonify(date_list)


if __name__ == "__main__":
    ocr = PaddleOCR(
    use_angle_cls=False,
    lang='en', 
    table=False, 
    use_mp=True,
    # image_dir='ocr_images',
    enable_mkldnn=True,
    use_gpu=False,
    max_batch_size = 20,
    total_process_num = os.cpu_count() * 2 - 1,
    )

  


  
    parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
    parser.add_argument("--port", default=9004, type=int, help="port number")
    args = parser.parse_args()
    
    app.run(host="0.0.0.0", port=args.port)   # debug=True causes Restarting with stat
