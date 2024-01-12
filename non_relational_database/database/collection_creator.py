from datetime import timedelta, datetime
import random
from faker import *
from non_relational_database.database.database_connection import database_connection

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


def create_prisons_with_buildings(num_prisons=3, num_buildings_per_prison=5):
    probability = 0.8
    prisons_collection = db['prisons']

    for _ in range(num_prisons):
        prison_data = {
            'prison_name': "Więzienie nr: " + str(random.randint(1, 100)),
            'city': fake.city(),
            'street': fake.street_name(),
            'building_nr': fake.building_number(),
            'apartment_nr': str(random.randint(1, 1000)) if random.random() < probability else None
        }

        buildings_data = create_buildings_for_prisons(num_buildings_per_prison)

        prison_data['buildings'] = buildings_data
        prisons_collection.insert_one(prison_data)


def create_buildings_for_prisons(num_buildings_per_prison):
    buildings_data = []

    for _ in range(num_buildings_per_prison):
        building_data = {
            'id_building': random.randint(1, 100),
            'city': fake.city(),
            'street': fake.street_address(),
            'building_nr': fake.building_number()
        }
        buildings_data.append(building_data)

    return buildings_data


def create_blocks(num_blocks_per_prison=8):
    blocks_collection = db['blocks']
    prisons_collection = db['prisons']

    prisons = list(prisons_collection.find())

    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Block.")

    for prison in prisons:
        prison_id = prison['_id']
        buildings = prison.get('buildings', [])

        if not buildings:
            continue

        for _ in range(num_blocks_per_prison):
            building = random.choice(buildings)

            block_data = {
                'block_name': random.choice(BLOCK_NAMES),
                'id_building': building['id_building'],
                'id_prison': prison_id,
            }

            blocks_collection.insert_one(block_data)


def create_cells(num_cells_per_block=10):
    cells_collection = db['cells']
    blocks_collection = db['blocks']

    blocks = list(blocks_collection.find())

    if len(blocks) == 0:
        raise Exception("No Blocks in the database. Can't create a Cell.")

    for block in blocks:
        block_id = block['_id']

        for i in range(num_cells_per_block):
            cell_type = random.choice(CELL_TYPES)
            cell_data = {
                'cell_nr': i,
                'cell_type': cell_type,
                'cell_capacity': random.randint(1, 10) if cell_type != 'Izolacyjna' else 1,
                'id_block': block_id,
                'id_prison': block['id_prison'],
            }

            cells_collection.insert_one(cell_data)


def create_stays_for_prisoner(prisoner_id_cell, num_stays_per_prisoner):
    stays_data = []

    for _ in range(num_stays_per_prisoner):
        stay_data = {
            'start_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            'end_date': (datetime.now() + timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            'id_cell': prisoner_id_cell,
        }

        stays_data.append(stay_data)
#     funkcja wywoływana z prisonera, coś jak budynki dla więzienia


def insert_collections():
    create_prisons_with_buildings()
    create_blocks()
    create_cells()

    print(db.list_collection_names())