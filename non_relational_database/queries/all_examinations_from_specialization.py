from pymongo import MongoClient

prisoner_first_name = "Jeremi"
prisoner_last_name = "Murat"
specialization_name = "Ginekolog"

client = MongoClient('mongodb://localhost:27017/')

result = client['Prison']['prisoners'].aggregate([
    {
        '$match': {
            'first_name': prisoner_first_name,
            'last_name': prisoner_last_name
        }
    },
    {
        '$unwind': '$examinations'
    },
    {
        '$lookup': {
            'from': 'doctors',
            'localField': 'examinations.id_doctor',
            'foreignField': '_id',
            'as': 'doctor_info'
        }
    },
    {
        '$match': {
            'doctor_info.specialization': specialization_name,
        }
    },
    {
        '$project': {
            'date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$examinations.examination_date'}},
            'type': '$examinations.examination_type',
            'result': '$examinations.examination_result',
            '_id': 0
        }
    }
])

if __name__ == '__main__':
    for res in result:
        print(res)
