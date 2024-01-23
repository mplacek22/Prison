from datetime import timedelta, datetime, time, date
import random

from bson import ObjectId
from faker import *
from non_relational_database.database.database_connection import database_connection

db = database_connection()

fake = Faker("pl_PL")

RANKS = [
    "Kapral",
    "Sierżant",
    "Starszy Sierżant",
    "Plutonowy",
    "Sierżant Sztabowy",
    "Młodszy Chorąży",
    "Chorąży",
    "Chorąży Sztabowy",
    "Podporucznik",
    "Porucznik",
    "Kapitan",
    "Major",
    "Podpułkownik",
    "Pułkownik",
    "Generał",
    ""
]

SPECIALIZATIONS = [
    "Kardiolog",
    "Pediatra",
    "Neurolog",
    "Dermatolog",
    "Ortopeda",
    "Ginekolog",
    "Gastroenterolog",
    "Radiolog",
    "Okulista",
    "Urolog",
    "Onkolog",
    "Pulmonolog",
    "Endokrynolog",
    "Nefrolog",
    "Reumatolog",
    "Psychiatra",
    "Anestezjolog",
    "Chirurg ogólny",
    "Specjalista chorób zakaźnych",
    "Hematolog"
]

EXAMINATIONS = dict([
    ("Masa ciała", lambda: str(round(random.uniform(40.0, 150.0), 1)) + " kg"),
    ("Temperatura ciała", lambda: str(round(random.uniform(36.0, 41.0), 1)) + " °C"),
    ("Poziom cukru we krwi", lambda: str(round(random.uniform(70, 120), 1))),
    ("Ciśnienie krwi", lambda: str(random.randint(90, 180)) + "/" + str(random.randint(60, 130)) + " mmHg"),
    ("Poziom cholesterolu", lambda: random.choice(["Wynik prawidłowy", "Podwyższony", "Zbyt niski"])),
    ("Wynik morfologii krwi", lambda: random.choice(["Normalny", "Anemia", "Leukocytoza"])),
    ("Poziom wapnia we krwi", lambda: str(round(random.uniform(8.0, 10.5), 2))),
    ("Poziom potasu we krwi", lambda: str(round(random.uniform(3.5, 5.5), 2))),
    ("Poziom sodu we krwi", lambda: str(round(random.uniform(135, 145), 2))),
    ("Wynik testu alergii", lambda: random.choice(["Brak alergii", "Alergia na pyłki", "Alergia na orzechy"])),
    ("Poziom witaminy D", lambda: str(round(random.uniform(20, 60), 2))),
    ("Poziom magnezu we krwi", lambda: str(round(random.uniform(1.5, 2.5), 2))),
    ("Poziom cynku we krwi", lambda: str(round(random.uniform(50, 120), 2))),
    ("Wynik prób wątrobowych",
     lambda: random.choice(["Wynik prawidłowy", "Podwyższone", "Podejrzenie uszkodzenia wątroby"])),
    ("Poziom trójglicerydów", lambda: str(round(random.uniform(50, 200), 1))),
    ("Poziom kreatyniny we krwi", lambda: str(round(random.uniform(0.5, 1.5), 2))),
    ("Kolonoskopia", lambda: random.choice(["Wynik negatywny", "Polip wykryty", "Nowotwór wykryty"])),
    ("Mammografia", lambda: random.choice(["Wynik negatywny", "Znaleziono nieprawidłowość"])),
    ("USG jamy brzusznej", lambda: random.choice(["Wynik prawidłowy", "Znaleziono nieprawidłowość"])),
    ("Elektrokardiogram", lambda: random.choice(["Wynik prawidłowy", "Zaburzenia rytmu", "Niedokrwienie serca"])),
    ("Konsultacja okulisty", lambda: random.choice(["Wynik prawidłowy", "Wymagana dalsza konsultacja"])),
    ("Badanie moczu", lambda: random.choice(["Wynik prawidłowy", "Obecność infekcji", "Inne nieprawidłowości"])),
    ("Test COVID-19", lambda: random.choice(["Wynik negatywny", "Wynik pozytywny", "Wymagane dalsze testy"]))
])

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


def create_prisons_with_buildings(num_prisons=50, num_buildings_per_prison=5):
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
            '_id': ObjectId(),
            'city': fake.city(),
            'street': fake.street_address(),
            'building_nr': fake.building_number()
        }
        buildings_data.append(building_data)

    return buildings_data


def create_blocks(num_blocks_per_prison=12):
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
                'id_building': building['_id'],
                'id_prison': prison_id,
            }

            blocks_collection.insert_one(block_data)


def create_cells(num_cells_per_block=15):
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


def create_doctors(num_doctors=30):
    for _ in range(num_doctors):
        pesel = fake.pesel()
        sex_digit = int(pesel[-2])
        is_female = sex_digit % 2 == 0
        doctor = {
            'PESEL': pesel,
            'name': fake.first_name_female() if is_female else fake.first_name_male(),
            'surname': fake.last_name_female() if is_female else fake.last_name_male(),
            'specialization': random.choice(SPECIALIZATIONS)
        }
        db['doctors'].insert_one(doctor)


def create_administrative_employees(num_administrative_employees_per_prison=5):
    prisons = list(db['prisons'].find())
    if len(prisons) == 0:
        raise Exception("No prisons in the database. Can't create an Administrative Employee.")

    for _ in range(num_administrative_employees_per_prison * len(prisons)):
        prison = random.choice(prisons)
        pesel = fake.pesel()
        sex_digit = int(pesel[-2])
        is_female = sex_digit % 2 == 0
        employee = {
            'PESEL': pesel,
            'name': fake.first_name_female() if is_female else fake.first_name_male(),
            'surname': fake.last_name_female() if is_female else fake.last_name_male(),
            'id_prison': prison['_id']
        }
        db['administrative_employees'].insert_one(employee)


def create_guards(num_guards_per_prison=30):
    prisons = list(db['prisons'].find())
    if len(prisons) == 0:
        raise Exception("No prisons in the database. Can't create a Guard.")

    for _ in range(num_guards_per_prison * len(prisons)):
        prison = random.choice(prisons)
        pesel = fake.pesel()
        sex_digit = int(pesel[-2])
        is_female = sex_digit % 2 == 0
        employee = {
            'PESEL': pesel,
            'name': fake.first_name_female() if is_female else fake.first_name_male(),
            'surname': fake.last_name_female() if is_female else fake.last_name_male(),
            'rank': random.choice(RANKS),
            'id_prison': prison['_id']
        }
        db['guards'].insert_one(employee)


def create_users():
    doctors = list(db['doctors'].find())
    guards = list(db['guards'].find())
    administrative_employees = list(db['administrative_employees'].find())
    for doctor in doctors:
        user = {
            'username': fake.user_name(),
            'password': fake.password(),
            'user_id': doctor['_id'],
            'user_type': 'doctor',
        }
        db['users'].insert_one(user)

    for guard in guards:
        user = {
            'username': fake.user_name(),
            'password': fake.password(),
            'user_id': guard['_id'],
            'user_type': 'guard',
        }
        db['users'].insert_one(user)

    for administrative_employee in administrative_employees:
        user = {
            'username': fake.user_name(),
            'password': fake.password(),
            'user_id': administrative_employee['_id'],
            'user_type': 'administrative_employee',
        }
        db['users'].insert_one(user)


def create_duties(start_datetime=datetime(year=2023, month=1, day=1, hour=6, minute=0, second=0),
                  end_datetime=datetime(year=2023, month=6, day=30, hour=22, minute=0, second=0)):
    blocks = list(db['blocks'].find())
    prisons = list(db['prisons'].find())

    if len(blocks) == 0:
        raise Exception("No blocks in database")

    if db['guards'].count_documents({}) == 0:
        raise Exception("No guards in database")

    duration = timedelta(hours=8)

    prisons_guards = {prison['_id']: list(db['guards'].find({'id_prison': prison['_id']})) for prison in prisons}
    prisons_blocks = {prison['_id']: list(db['blocks'].find({'id_prison': prison['_id']})) for prison in prisons}

    while start_datetime < end_datetime:
        for prison, p_blocks in prisons_blocks.items():
            if len(p_blocks) == 0:
                continue

            duties = []
            for block in p_blocks:
                duty = {
                    'block': block,
                    'start_date': start_datetime,
                    'end_date': start_datetime + duration,
                    'ids_guards': [],
                }

                duties.append(duty)

            available_guards = prisons_guards[prison]
            n = len(available_guards)

            if n < len(duties):
                raise Exception("No guards available for duty")

            for duty in duties:
                idx = random.randint(0, n - 1)
                duty['ids_guards'].append(available_guards[idx]['_id'])
                available_guards[idx], available_guards[n - 1] = available_guards[n - 1], available_guards[idx]
                n -= 1
            for i in range(n):
                duty = random.choice(duties)
                duty['ids_guards'].append(available_guards[i]['_id'])

            db['duties'].insert_many(duties)

        start_datetime += duration


def create_examinations(min_num_examinations_per_prisoner=1, max_num_examinations_per_prisoner=20):
    doctors = list(db['doctors'].find())
    examinations = []
    for _ in range(random.randint(min_num_examinations_per_prisoner, max_num_examinations_per_prisoner)):
        examination_date = fake.date_time_between(start_date=datetime(year=2020, month=1, day=1),
                                                  end_date=datetime(year=2023, month=6, day=30))

        examination_type = random.choice(list(EXAMINATIONS.keys()))
        result = EXAMINATIONS[examination_type]

        examination = {
            'examination_date': examination_date,
            'id_doctor': random.choice(doctors)['_id'],
            'examination_type': examination_type,
            'examination_result': result()
        }
        examinations.append(examination)
    return examinations


def create_stays(prison_id, admission_date, num_stays_per_prisoner=2):
    cells_collection = db['cells']
    cells_in_prison = list(cells_collection.find({'id_prison': prison_id}))

    if not cells_in_prison:
        raise Exception("No cells found in the prison.")

    stays_data = []
    current_date = admission_date

    for _ in range(num_stays_per_prisoner):
        cell = random.choice(cells_in_prison)
        cell_id = cell['_id']

        stay_duration = random.randint(1, 735)
        stay_data = {
            'id_cell': cell_id,
            'start_date': current_date.strftime("%Y-%m-%d"),
            'end_date': (current_date + timedelta(days=stay_duration)).strftime("%Y-%m-%d"),
        }

        stays_data.append(stay_data)
        current_date = current_date + timedelta(days=stay_duration + 1)

    stays_data[-1]['end_date'] = None
    return stays_data


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


def create_contact_person():
    contact_person_data = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'kinship': random.choice(KINSHIPS),
        'phone_nr': fake.phone_number()
    }
    return contact_person_data


def create_prisoners(num_prisoners=10000):
    prisoners_collection = db['prisoners']
    prisons_collection = db['prisons']
    prisons_list = list(prisons_collection.find())

    if not prisons_list:
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

        # random_prison = list(prisons.aggregate([{'$sample': {'size': 1}}]))
        prison = random.choice(prisons_list)
        prison_id = prison['_id']

        prisoner_data = {
            'pesel': pesel,
            'first_name': fake.first_name_female() if is_female else fake.first_name_male(),
            'last_name': fake.last_name_female() if is_female else fake.last_name_male(),
            'admission_date': admission_date,
            'contact_person': create_contact_person(),
            'height': random.randint(150, 210) if random.random() < 0.8 else None,
            'blood_group': random.choice(BLOOD_GROUPS) if random.random() < 0.8 else None,
            'sex': 'F' if is_female else 'M',
            'id_prison': prison_id,
            'furloughs': create_furloughs(),
            'visits': create_visits(),
            'examinations': create_examinations(),
            'sentences': create_sentences(),
            'stays': create_stays(prison_id, admission_date),
        }
        prisoners_collection.insert_one(prisoner_data)


def insert_collections():
    create_prisons_with_buildings()
    create_blocks()
    create_cells()
    create_doctors()
    create_administrative_employees()
    create_guards()
    create_users()
    create_duties()
    create_prisoners()

    print(db.list_collection_names())
