import pymongo


def database_connection():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["Prison2"]
    return db
