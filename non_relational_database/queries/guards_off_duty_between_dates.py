# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from datetime import datetime, timezone

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Run the aggregation query
aggregation_result = client['Prison']['duties'].aggregate([
    {
        '$match': {
            'start_date': {
                '$gte': datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            },
            'end_date': {
                '$lte': datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
            }
        }
    },
    {
        '$unwind': {
            'path': '$ids_guards'
        }
    },
    {
        '$group': {
            '_id': None,
            'on_duty_guards': {
                '$addToSet': '$ids_guards'
            }
        }
    }
])

# Extract on-duty guards from the cursor
on_duty_guards = []
for doc in aggregation_result:
    on_duty_guards.extend(doc.get('on_duty_guards', []))

# Query for off-duty guards
off_duty_guards = client['Prison']['guards'].find({
    '_id': {
        '$nin': on_duty_guards  # Select guards whose IDs are not in the on-duty list
    }
})


# Process or print the off-duty guards
if __name__ == '__main__':
    for guard in off_duty_guards:
        print(guard)
