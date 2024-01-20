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
        '$unwind': {
            'path': '$ids_guards',
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
        '$group': {
            '_id': '$ids_guards',
            'total_hours': {'$sum': 'work_hours'},
        }
    },
    {
        '$sort': {'total_hours': -1}
    },
    {
        '$limit': 5
    },
])

duty_guards = [all_guards['_id'] for all_guards in result]

guards = client['Prison']['guards'].find({
    '_id': {'$in': duty_guards},
})

if __name__ == '__main__':
    for guard in guards:
        print(guard)

