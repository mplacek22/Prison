from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

result1 = client['Prison']['prisoners'].find({
    'furloughs': {'$size': 0}
})

result = client['Prison']['prisoners'].aggregate([
    {
        '$match': {
            'furloughs': {'$size': 0}
        }
    },
    {
        '$project': {
            'first_name': 1,
            'last_name': 1,
            'pesel': 1,
            '_id': 0
        }
    }
])


if __name__ == '__main__':
    for res in result:
        print(res)