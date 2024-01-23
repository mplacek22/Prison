from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

current_month_start = datetime(2023, 2, 1)
next_month_start = datetime(current_month_start.year, current_month_start.month + 1, 1)

result = client['Prison']['duties'].aggregate([
    {
        '$match': {
            'start_date': {
                '$gte': current_month_start
            },
            'end_date': {
                '$lt': next_month_start
            },
        }
    },
    {
        '$addFields': {
            'work_hours': {
                '$divide': [{'$subtract': ['$end_date', '$start_date']}, 3600000]
            }
        }
    },
    {
        '$unwind': {
            'path': '$ids_guards',
        }
    },
    {
        '$group': {
            '_id': '$ids_guards',
            'total_hours': {'$sum': '$work_hours'},
        }
    },
    {
        '$sort': {'total_hours': -1}
    },
    {
        '$limit': 5
    },
    {
        '$lookup': {
            'from': 'guards',
            'localField': '_id',
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
            'total_hours': 1,
            '_id': 0,
        }
    },
])

if __name__ == '__main__':
    for res in result:
        print(res)

