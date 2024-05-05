# # from common.utils import CacheHelper,MongoHelper
# from django.http import response
# import inspection
import numpy as np
import cv2 
from numpy import array
# import json
# import base64
# import multiprocessing
# import sys
# from pymongo import MongoClient
# from bson import ObjectId
# from livis import settings as settings
# from livis.settings import BASE_URL
# from livis.settings import *
import os
import time
import datetime
# from dateutil import tz
# import requests
# from datetime import datetime
# from mongohelper import MongoHelper
from base64 import decodebytes
import pandas as pd
import os
from pyzbar.pyzbar import decode
from PIL import Image

def barcode_scanner():
    img=cv2.imread("D:\\n.jpg")
    # print("img",img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    q2c_barcode = ""
    p = decode(img)
    # print(p)
    # for i in p:
    k = p[0][0]
        # if k:
        #     break
    try:
        q2c_barcode = k.decode('UTF-8')
    except Exception as e:
        print(e)
        pass
    return q2c_barcode

a=barcode_scanner()
print(a)    