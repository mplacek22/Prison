from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

FILING = 0.8

result = client['Prison']['prisoners'].aggregate([
    {
        '$unwind': '$stays'
    },
    {
        '$match': {
            'stays.end_date': None
        }
    },
    {
        '$lookup': {
            'from': 'cells',
            'localField': 'stays.id_cell',
            'foreignField': '_id',
            'as': 'cell_info'
        }
    },
    {
        '$unwind': '$cell_info'
    },
    {
        '$group': {
            '_id': '$cell_info._id',
            'id_prison': {'$first': '$cell_info.id_prison'},
            'capacity': {'$first': '$cell_info.cell_capacity'},
            'count': {'$sum': 1}
        }
    },
    {
        '$group': {
            '_id': '$id_prison',
            'filling': {'$avg': {'$divide': ['$count', '$capacity']}}
        }
    },
    {
        '$match': {
            'filling': {'$lte': FILING}
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
            'filling': 1,
            '_id': 0
        }
    },
])

if __name__ == '__main__':
    for res in result:
        print(res)
