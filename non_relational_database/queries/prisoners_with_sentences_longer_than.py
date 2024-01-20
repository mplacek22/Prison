from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

sentence_duration = 1825  # 5 years
specific_prison_name = 'Więzienie nr: 4'

prisoners_with_long_sentences = client['Prison']['prisoners'].aggregate([
    {
        '$unwind': {
            'path': '$sentences',
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
            'sentences.stay_duration_days': {
                '$exists': True,
                '$ne': None,
                '$gte': sentence_duration
            },
            'prison_info.prison_name': specific_prison_name
        }
    },
    {
        '$project': {
            'first_name': 1,
            'last_name': 1,
            'admission_date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$admission_date'}},
            'sentence_duration_days': '$sentences.stay_duration_days'
        }
    }
])

if __name__ == '__main__':
    print(specific_prison_name)
    for prisoner in prisoners_with_long_sentences:
        print(prisoner)
