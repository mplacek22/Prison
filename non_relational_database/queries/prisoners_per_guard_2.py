# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from datetime import datetime, timezone

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

results = client['Prison']['prisoners'].aggregate([
    {
        '$group': {
            '_id': '$id_prison',
            'prisoners_count': {'$sum': 1}
        }
    },
    {
        '$lookup': {
            'from': 'guards',
            'localField': '_id',
            'foreignField': 'id_prison',
            'as': 'guards'
        }
    },
    {
        '$set': {
            'guards_count': {'$size': '$guards'}
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
            '_id': 0,
            'prison_name': '$prison_info.prison_name',
            'prisoners_count': 1,
            'guards_count': 1,
            'prisoners_per_guard': {'$divide': ['$prisoners_count', '$guards_count']}
        }
    }

])

# Output result
if __name__ == '__main__':
    for res in results:
        print(res)
