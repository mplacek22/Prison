from datetime import timedelta, datetime, time, date
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

KINSHIPS = [
    "Rodzic",
    "Dziadek",
    "Dziecko",
    "Wnuk",
    "Rodzeństwo",
    "Małżonek",
    "Krewny",
    "Znajomy",
    "Nieznajomy",
]

GENDERS = ['F', 'M']

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', '0+', '0-']


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


def create_stays_for_prisoner(prisoner_id_cell,
                              num_stays_per_prisoner):  # TODO: change to random cell from specified prison
    stays_data = []

    for _ in range(num_stays_per_prisoner):
        stay_data = {
            'start_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            'end_date': (datetime.now() + timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            'id_cell': prisoner_id_cell,
        }

        stays_data.append(stay_data)


#     funkcja wywoływana z prisonera, coś jak budynki dla więzienia


def create_sentences(sentences_count_weights=(0.5, 0.2, 0.15, 0.1, 0.05)):
    sentences_count = random.choices(range(1, len(sentences_count_weights) + 1),
                                     weights=sentences_count_weights)[0]
    sentences = []
    for _ in range(sentences_count):
        duration = random.randint(1, 9200)
        if duration > 9150:
            duration = 20000
        sentences.append({
            'article': str(random.randint(1, 400)),
            'paragraph': random.randint(1, 15),
            'stay_duration_days': duration
        })
    return sentences


def create_furloughs(num_furloughs_per_prisoner=2):
    furloughs = []
    for _ in range(num_furloughs_per_prisoner):
        start_date = fake.date_between(start_date=date(year=2020, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = time(hour=random.randint(8, 19), minute=random.randint(0, 59),
                          second=random.randint(0, 59))

        end_time = time(hour=random.randint(8, 19), minute=random.randint(0, 59),
                        second=random.randint(0, 59))

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(start_date + timedelta(days=random.randint(1, 14)), end_time)

        furlough_data = {
            'start_date': start_datetime,
            'end_date': end_datetime
        }
        furloughs.append(furlough_data)
    return furloughs


def create_visits(num_visits_per_prisoner=3):
    visits = []
    for _ in range(num_visits_per_prisoner):
        start_date = fake.date_between(start_date=date(year=2020, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = time(hour=random.randint(8, 19), minute=random.randint(0, 59),
                          second=random.randint(0, 59))

        duration = timedelta(seconds=random.randint(15 * 60, 4 * 60 * 60))

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = start_datetime + duration

        visit_data = {
            'start_date': start_datetime,
            'end_date': end_datetime,
            'first_name': fake.first_name(),
            'last_name': fake.last_name()
        }
        visits.append(visit_data)
    return visits


def create_contact_persons(num_contact_persons_per_prisoner=2):
    contact_persons = []
    for _ in range(num_contact_persons_per_prisoner):
        contact_person_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'kinship': random.choice(KINSHIPS),
            'phone_nr': fake.phone_number()
        }
        contact_persons.append(contact_person_data)
    return contact_persons


def create_contact_person():
    contact_person_data = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'kinship': random.choice(KINSHIPS),
        'phone_nr': fake.phone_number()
    }
    return contact_person_data


def create_prisoners(num_prisoners=100):
    prisoners_collection = db['prisoners']
    prisons = db['prisons']
    if prisons.count_documents({}) == 0:
        raise Exception("No prisons in the database. Can't create a Prisoner.")

    for _ in range(num_prisoners):
        # Generate prisoner data
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
        pesel = fake.pesel(date_of_birth=date_of_birth)
        sex_digit = int(pesel[-2])
        is_female = sex_digit % 2 == 0
        sentences = create_sentences()
        sentence_time = sum([sentence['stay_duration_days'] for sentence in sentences])
        admission_date = fake.date_time_between(
            start_date=max(datetime.combine(date_of_birth + timedelta(days=365 * 17), time(hour=0, minute=0)),
                           datetime(year=2023, month=6, day=30) - timedelta(days=sentence_time)),
            end_date=datetime(year=2023, month=6, day=30)
        )
        random_prison = list(prisons.aggregate([{ '$sample': { 'size': 1 } }]))
        prisoner_data = {
            'pesel': pesel,
            'first_name': fake.first_name_female() if is_female else fake.first_name_male(),
            'last_name': fake.last_name_female() if is_female else fake.last_name_male(),
            'admission_date': admission_date,
            'contact_person': create_contact_person(),
            'height': random.randint(150, 210) if random.random() < 0.8 else None,
            'blood_group': random.choice(BLOOD_GROUPS) if random.random() < 0.8 else None,
            'sex': 'F' if is_female else 'M',
            'id_prison': str(random_prison[0].get('_id')),
            'furloughs': create_furloughs(),
            'visits': create_visits(),
            'examinations': [],  # TODO create_examinations()
            'sentences': create_sentences(),
            'stays': [],
        }
        prisoners_collection.insert_one(prisoner_data)


def insert_collections():
    create_prisons_with_buildings()
    create_blocks()
    create_cells()
    create_prisoners()

    print(db.list_collection_names())
