from pymongo import MongoClient

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://localhost:27017/')
result = client['Prison']['prisoners'].aggregate([
    {
        '$lookup': {
            'from': 'prisons', 
            'localField': 'id_prison', 
            'foreignField': '_id', 
            'as': 'prison_info'
        }
    }, {
        '$unwind': {
            'path': '$prison_info', 
            'includeArrayIndex': '0', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$group': {
            '_id': '$id_prison', 
            'prison_name': {
                '$first': '$prison_info.prison_name'
            }, 
            'number_of_prisoners': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'prison_id': '$_id', 
            'prison_name': 1, 
            'number_of_prisoners': 1
        }
    }
])