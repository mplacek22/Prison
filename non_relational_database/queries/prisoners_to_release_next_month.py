from datetime import datetime, timedelta
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

current_date = datetime.now()
next_month_start = datetime(current_date.year, current_date.month + 1, 1)
next_month_end = datetime(current_date.year, current_date.month + 2, 1) - timedelta(days=1)

specific_prison_name = 'Więzienie nr: 76'  # execute all_prisoners_to_release_next_month to find prison

prisoners_to_release = client['Prison']['prisoners'].aggregate([
    {
        '$unwind': {
            'path': '$sentences',
        }
    },
    {
        '$match': {
            'sentences.stay_duration_days': {
                '$exists': True,
                '$ne': None
            }
        }
    },
    {
        '$addFields': {
            'release_date': {
                '$add': ['$admission_date', {'$multiply': ['$sentences.stay_duration_days', 24, 3600000]}]
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
        '$match': {
            'release_date': {
                '$gte': next_month_start,
                '$lte': next_month_end
            },
            'prison_info.prison_name': specific_prison_name
        }
    },
    {
        '$project': {
            'first_name': 1,
            'last_name': 1,
            'admission_date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$admission_date'}},
            'release_date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$release_date'}}
        }
    }
])

if __name__ == '__main__':
    print(specific_prison_name)
    for prisoner in prisoners_to_release:
        print(prisoner)



