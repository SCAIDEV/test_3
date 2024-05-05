from pymongo import MongoClient

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

MONGO_SERVER_HOST = "localhost"
MONGO_SERVER_PORT = 27017
MONGO_DB = "mrp"
MONGO_COLLECTIONS = {}

@singleton
class MongoHelper:
    client = None
    def __init__(self):
        if not self.client:
            self.client = MongoClient(host=MONGO_SERVER_HOST, port=MONGO_SERVER_PORT)
        self.db = self.client[MONGO_DB]

    def getDatabase(self):
        return self.db

    def getCollection(self, cname, create=False, codec_options=None):
        _DB = MONGO_DB
        DB = self.client[_DB]
        if cname in MONGO_COLLECTIONS:
            if codec_options:
                return DB.get_collection(MONGO_COLLECTIONS[cname], codec_options=codec_options)
            return DB[MONGO_COLLECTIONS[cname]]
        else:
            return DB[cname]
