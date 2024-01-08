#  prisoners with sentence of 10 years or more
def query_1(db):
    return db.Prisoners.find({"sentences.stay_duration_days": {"$gte": 10 * 365}})


# prisoner with given name and surname
def query_2(db, name, surname):
    return db.Prisoners.find({"name": name, "surname": surname})


# doctor whose specialization is from given list
def query_3(db, specializations):
    return db.Doctors.find({"specialization": {"$in": specializations}})


# prisoners who was in more than given number of cells
def query_4(db, cells):
    return db.Prisoners.find({"stays": {"$size": {"$gt": cells}}})


# duties on given block with given number of guards
def query_5(db, block, guards):
    return db.Duties.find({"block": block, "guards_ids": {"$size": guards}})


# cells with capacity between given numbers
def query_6(db, min_capacity, max_capacity):
    return db.Cells.find({"capacity": {"$gt": min_capacity, "$lt": max_capacity}})


# prisoners without furloughs or visits
def query_7(db):
    return db.Prisoners.find({"$or": [{"furloughs": []}, {"visits": []}]})
