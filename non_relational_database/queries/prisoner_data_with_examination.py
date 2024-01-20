from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

exam_name = "Mammografia"
prisoner_first_name = "Konrad"
prisoner_last_name = "Kumorek"

result = client['Prison']['prisoners'].aggregate([
    {
        '$match': {
            'first_name': prisoner_first_name,
            'last_name': prisoner_last_name
        }
    },
    {
        '$unwind': {
            'path': '$examinations',
        }
    },
    {
        '$match': {
            'examinations.examination_type': exam_name
        }
    },
    {
        '$project': {
            '_id': 1,
            'pesel': 1,
            'first_name': 1,
            'last_name': 1,
            'admission_date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$admission_date'}},
            'height': 1,
            'blood_group': 1,
            'sex': 1,
            'id_prison': 1,
            'furloughs': 1,
            'visits': 1,
            'examinations': {
                '$cond': {
                    'if': {'$eq': ['$examinations.examination_type', exam_name]},
                    'then': '$examinations',
                    'else': []
                }
            },
            'sentences': 1,
            'stays': 1
        }
    }
])

if __name__ == '__main__':
    for prisoner in result:
        print(prisoner)

