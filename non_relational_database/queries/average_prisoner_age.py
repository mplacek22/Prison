from datetime import datetime

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

result = client['Prison']['prisoners'].aggregate([
    {
        '$set': {
            'age': {
                '$subtract': [
                    {'$year': '$$NOW'},
                    {'$add': [
                        {'$cond': {
                            'if': {'$gt': [{'$toInt': {'$substr': ['$pesel', 2, 2]}}, 20]},
                            'then': 2000,
                            'else': 1900
                        }},
                        {'$toInt': {'$substr': ['$pesel', 0, 2]}}
                    ]}
                ]
            }
        }
    },
    {
        '$group': {
            '_id': '$id_prison',
            'average_age': {'$avg': '$age'}
        }
    },
    {
        '$lookup': {
            'from': 'prisons',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'prison_info'
        }
    },
    {
        '$unwind': '$prison_info'
    },
    {
        '$project': {
            'prison_name': '$prison_info.prison_name',
            'average_age': 1,
            '_id': 0,
        }
    }
])

if __name__ == '__main__':
    for res in result:
        print(res)