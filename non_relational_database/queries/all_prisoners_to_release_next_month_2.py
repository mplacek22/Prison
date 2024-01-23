from datetime import datetime, timedelta
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

current_date = datetime.now()
next_month_start = datetime(current_date.year, current_date.month + 1, 1)
next_month_end = datetime(current_date.year, current_date.month + 2, 1) - timedelta(days=1)

prisoners_to_release = client['Prison']['prisoners'].aggregate([
    # {
    #     '$unwind': {
    #         'path': '$sentences',
    #     }
    # },
    {
        '$match': {
            'sentences.stay_duration_days': {
                '$ne': None
            }
        }
    },
    {
        '$addFields': {
            'release_date': {
                '$add': ['$admission_date', {'$multiply': [{'$sum': '$sentences.stay_duration_days'}, 24, 3600000]}]
            }
        }
    },
    {
        '$match': {
            'release_date': {
                '$gte': next_month_start,
                '$lte': next_month_end
            }
        }
    },
    {
        '$lookup': {
            'from': 'prisons',
            'localField': 'id_prison',
            'foreignField': '_id',
            'as': 'prison_info'
        }
    },
    {
        '$unwind': '$prison_info'
    },

    {
        '$project': {
            'first_name': 1,
            'last_name': 1,
            'admission_date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$admission_date'}},
            'release_date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$release_date'}},
            'prison_name': '$prison_info.prison_name'
        }
    }
])

if __name__ == '__main__':
    for prisoner in prisoners_to_release:
        print(prisoner)