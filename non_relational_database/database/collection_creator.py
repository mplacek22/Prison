from datetime import date, timedelta, time, datetime
import random
from faker import *
from non_relational_database.database.nrd_main import database_connection

db = database_connection()

Faker.seed(123)
random.seed(123)
fake = Faker("pl_PL")

CELL_TYPES = [
    "Męska",
    "Żeńska",
    "Izolacyjna"
]

BLOCK_NAMES = [
    'Izolatki',
    'Nieletni',
    'Niski Poziom Zabezpieczeń',
    'Wysoki Poziom Zabezpieczeń',
    'Chororzy Psychicznie',
    'Pracujący Społecznie'
]


def create_prisons(num_prisons=3):
    probability = 0.8
    prisons_collection = db['prisons']

    for _ in range(num_prisons):
        prison_data = {
            'penitentiary_name': "Więzienie nr: " + str(random.randint(1, 100)),
            'city': fake.city(),
            'street': fake.street_name(),
            'building_nr': fake.building_number(),
            'apartment_nr': str(random.randint(1, 1000)) if random.random() < probability else None
        }

        prisons_collection.insert_one(prison_data)


def create_buildings(num_building_per_prison=5):
    buildings_collection = db['buildings']
    prisons_collection = db['prisons']

    prison_ids = [p['_id'] for p in prisons_collection.find()]

    if len(prison_ids) == 0:
        raise Exception("No Prisons in the database. Can't create a Building.")

    additional_buildings_count = int(len(prison_ids) * num_building_per_prison)

    for prison_id in prison_ids + random.choices(prison_ids, k=additional_buildings_count):
        building_data = {
            'city': fake.city(),
            'street': fake.street_address(),
            'building_nr': str(random.randint(1, 50)),
            'id_prison': prison_id
        }
        buildings_collection.insert_one(building_data)


def create_cells(num_cells_per_block=10):
    cells_collection = db['cells']
    blocks_collection = db['blocks']

    block_ids = [b['_id'] for b in blocks_collection.find()]

    if len(block_ids) == 0:
        raise Exception("No Blocks in the database. Can't create a Cell.")

    for i in range(num_cells_per_block):
        cell_type = random.choice(CELL_TYPES)
        cell_data = {
            'cell_nr': i,
            'cell_type': cell_type,
            'cell_capacity': random.randint(1, 10) if cell_type != 'Izolacyjna' else 1,
            'id_block': random.choice(block_ids),
        }

        cells_collection.insert_one(cell_data)


def create_blocks(num_blocks_per_prison=8):
    blocks_collection = db['blocks']
    prisons_collection = db['prisons']
    buildings_collection = db['buildings']

    prisons = list(prisons_collection.find())

    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Block.")

    building_ids = [b['_id'] for b in buildings_collection.find()]

    blocks_count = int(len(prisons) * num_blocks_per_prison)
    for i in range(blocks_count):
        block_data = {
            'block_name': random.choice(BLOCK_NAMES),
            'id_building': random.choice(building_ids),
        }

        blocks_collection.insert_one(block_data)


def create_stays(num_stays_per_prisoner=3):
    stays_collection = db['stays']
    prisoners_collection = db['prisoners']
    cells_collection = db['cells']

    prisoners = list(prisoners_collection.find())

    if len(prisoners) == 0:
        raise Exception("No Prisoners in the database. Can't create a Stay.")

    cell_ids = [c['_id'] for c in cells_collection.find()]

    for prisoner in prisoners:
        for _ in range(num_stays_per_prisoner):
            stay_data = {
                'id_cell': random.choice(cell_ids),
                'start_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
                'end_date': (datetime.now() + timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
            }

            stays_collection.insert_one(stay_data)


def insert_collectons():
    create_prisons()
    create_buildings()
    create_blocks()
    create_cells()
