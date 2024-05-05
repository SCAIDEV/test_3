import neoapi
import redis
import sys
sys.path.insert(0, '../')
import time
import cv2
import redis
import pickle

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class CacheHelper():
    def __init__(self):
        # self.redis_cache = redis.StrictRedis(host="164.52.194.78", port="8080", db=0, socket_timeout=1)
        #self.redis_cache = redis.StrictRedis(host='13.235.133.102', port=5051, db=0, socket_timeout=1)
        self.redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0, socket_timeout=1)
        #s.REDIS_CLIENT_HOST
        print("REDIS CACHE UP!")

    def get_redis_pipeline(self):
        return self.redis_cache.pipeline()
    
    def set_json(self, dict_obj):
        try:
            k, v = list(dict_obj.items())[0]
            v = pickle.dumps(v)
            return self.redis_cache.set(k, v)
        except redis.ConnectionError:
            return None

    def get_json(self, key):
        try:
            temp = self.redis_cache.get(key)
            #print(temp)\
            if temp:
                temp= pickle.loads(temp)
            return temp
        except redis.ConnectionError:
            return None
        return None

    def execute_pipe_commands(self, commands):
        #TBD to increase efficiency can chain commands for getting cache in one go
        return None


try:
    camera_ip_bottom_three = "192.168.1.2"
    camera_bottom_three = neoapi.Cam() #site
    camera_bottom_three.Connect(camera_ip_bottom_three)
    #camera_bottom_three.f.Width = 5472
    #camera_bottom_three.f.Height = 3648
    #camera_bottom_three.f.OffsetY = 0 
    # camera_bottom_three.f.ExposureTime.Set(14000)
    # camera_bottom_three.f.Gain.Set(2.5)
    # camera_bottom_three.f.ExposureAuto.SetString('Off')
    # camera_bottom_three.f.PixelFormat.SetString('BayerRG8')
    # CacheHelper().set_json({'cam_health':1})
    #camera.f.AcquisitionFrameRateEnable.value = True
    #camera.f.AcquisitionFrameRate.value = 10
except Exception as e:
    print("cannot connect to camera or set it parameters")
    print(e)



while True:
   

    camera_bottom_three_trigger = CacheHelper().get_json("camera_trigger")

    if camera_bottom_three_trigger:
        start = time.time()
        while True:
          
                try:
                    imgarray_bottom_three = camera_bottom_three.GetImage().GetNPArray()
                    imgarray_bottom_three = cv2.cvtColor(imgarray_bottom_three,cv2.COLOR_BAYER_RG2RGB)
                    print("Image",imgarray_bottom_three)
                    # imgarray_bottom_three = cv2.imread('bottom_three_original.bmp')
                    # cv2.imwrite('bottom_three_original_src.png',imgarray_bottom_three)
                    end = time.time() - start
                    print("published in ::",str(end))
                    start = time.time()
                    CacheHelper().set_json({"camera_original" : imgarray_bottom_three})
                    CacheHelper().set_json({'cam_health':imgarray_bottom_three})
                    CacheHelper().set_json({"camera_trigger":False})
                    break
                    
                except Exception as e:
                    print("cannot connect to Redis")
                    print(e)
           
                
    else:
        continue
    