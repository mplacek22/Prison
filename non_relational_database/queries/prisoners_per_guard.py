# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from datetime import datetime, timezone

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

prisoners_per_prison = client['Prison']['prisoners'].aggregate([
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

guards_per_prison = client['Prison']['guards'].aggregate([
    {
        '$group': {
            '_id': '$id_prison',
            'guards_count': {'$sum': 1}
        }
    }
])

# Convert lists to dictionaries for easier processing
prisoners_dict = {doc['prison_id']: {'count': doc['number_of_prisoners'], 'prison_name': doc['prison_name']} for doc in prisoners_per_prison}
guards_dict = {doc['_id']: doc['guards_count'] for doc in guards_per_prison}

# Calculate prisoners per guard
prisoners_per_guard = {}
for prison_id, info in prisoners_dict.items():
    guard_count = guards_dict.get(prison_id, 0)
    if guard_count > 0:
        prisoners_per_guard[info['prison_name']] = info['count'] / guard_count
    else:
        prisoners_per_guard[info['prison_name']] = None  # Handle case where there are no guards

# Output result
if __name__ == '__main__':
    for prison_name, ratio in prisoners_per_guard.items():
        print(f"Prison name: {prison_name}, Prisoners per guard: {ratio}")
