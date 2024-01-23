# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from datetime import datetime, timezone

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Run the aggregation query
result = client['Prison']['duties'].aggregate([
    {
        '$match': {
            'start_date': {
                '$gte': datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            },
            'end_date': {
                '$lte': datetime(2023, 1, 1, 16, 0, 0, tzinfo=timezone.utc)
            }
        }
    },
    {
        '$unwind': {
            'path': '$ids_guards'
        }
    },
    {
        '$group': {
            '_id': None,
            'on_duty_guards': {
                '$addToSet': '$ids_guards'
            }
        }
    },
    {
        "$unionWith": {
            "coll": "guards",
            "pipeline": [
                {
                    "$group": {
                        "_id": None,
                        "guards": {
                            "$addToSet": "$_id"
                        }
                    }
                }
            ]
        }
    },
    {
        '$group': {
            '_id': None,
            'on_duty_guards': {
                '$first': '$on_duty_guards'
            },
            'all_guards': {
                '$last': '$guards'
            }
        }
    },
    {
        '$project': {
            '_id': 0,
            'off_duty_guards': {
                '$setDifference': ['$all_guards', '$on_duty_guards']
            }
        }
    },
    {
        '$unwind': '$off_duty_guards'
    },
    {
        '$lookup': {
            'from': 'guards',
            'localField': 'off_duty_guards',
            'foreignField': '_id',
            'as': 'guard_info'
        }
    },
    {
        '$unwind': '$guard_info'
    },
    {
        '$project': {
            'first_name': '$guard_info.name',
            'last_name': '$guard_info.surname',
            "PESEL": "$guard_info.PESEL",
            '_id': 0
        }
    }
])

# Process or print the off-duty guards
if __name__ == '__main__':
    for guard in result:
        print(guard)
