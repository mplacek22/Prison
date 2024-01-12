import pymongo

from non_relational_database.database.collection_creator import insert_collectons


def database_connection():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["Prison"]
    return db


def run():
    database_connection()
    insert_collectons()


if __name__ == '__main__':
    run()
