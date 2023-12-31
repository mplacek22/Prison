from collections import deque
from contextlib import suppress
from datetime import date, timedelta, time
import random
from faker import *
from relational_database.database.entities import *

Faker.seed(123)
random.seed(123)

fake = Faker("pl_PL")

CELL_TYPES = [
    "Męska",
    "Żeńska",
    "Izolacyjna"
]

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
    "Generał"
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


@db_session
def create_examination_types():
    for examination_type in EXAMINATIONS:
        ExaminationType(examination_type=examination_type)

@db_session
def create_administrative_employees(num_admins_per_prison=15):
    prison_ids = select(p.id_prison for p in Prison)[:]
    if len(prison_ids) == 0:
        raise Exception("No Prisons in the database. Can't create an AdministrativeEmployee.")

    admin_count = int(len(prison_ids) * num_admins_per_prison)
    for i in range(1, admin_count + 1):
        pesel = fake.pesel()
        sex_digit = int(pesel[-2])
        is_female = sex_digit % 2 == 0
        admin_data = {
            'pesel': pesel,
            'name': fake.first_name_female() if is_female else fake.first_name_male(),
            'surname': fake.last_name_female() if is_female else fake.last_name_male(),
            'id_prison': random.choice(prison_ids)
        }
        AdministrativeEmployee(**admin_data)


@db_session
def create_doctors(num_doctors=100):
    specialization_ids = select(s.id_specialization for s in Specialization)[:]

    if len(specialization_ids) == 0:
        raise Exception("No Specializations in the database. Can't create a Doctor.")

    for i in range(1, 1 + num_doctors):
        pesel = fake.pesel()
        sex_digit = int(pesel[-2])
        is_female = sex_digit % 2 == 0
        doctor_data = {
            'pesel': pesel,
            'name': fake.first_name_female() if is_female else fake.first_name_male(),
            'surname': fake.last_name_female() if is_female else fake.last_name_male(),
            'id_specialization': random.choice(specialization_ids)
        }
        Doctor(**doctor_data)


@db_session
def create_users():
    for admin in AdministrativeEmployee.select():
        User(username=fake.unique.user_name(), password=fake.password(length=random.randint(8, 30)),
             id_employee=admin.id_employee)
    for guard in Guard.select():
        User(username=fake.unique.user_name(), password=fake.password(length=random.randint(8, 30)),
             id_guard=guard.id_guard)
    for doctor in Doctor.select():
        User(username=fake.unique.user_name(), password=fake.password(length=random.randint(8, 30)),
             id_doctor=doctor.id_doctor)


@db_session
def create_furloughs(num_furloughs_per_prisoner=2):
    prisoner_ids = select(prisoner.id_prisoner for prisoner in Prisoner)[:]

    if len(prisoner_ids) == 0:
        raise Exception("No prisoners in database")

    furloughs_count = int(len(prisoner_ids) * num_furloughs_per_prisoner)

    for furlough_id in range(1, furloughs_count + 1):
        start_date = fake.date_between(start_date=date(year=2020, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = time(hour=random.randint(8, 19), minute=random.randint(0, 59),
                          second=random.randint(0, 59))

        end_time = time(hour=random.randint(8, 19), minute=random.randint(0, 59),
                        second=random.randint(0, 59))

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(start_date + timedelta(days=random.randint(1, 14)), end_time)

        furlough_data = {
            'id_prisoner': random.choice(prisoner_ids),
            'start_date': start_datetime,
            'end_date': end_datetime
        }

        Furlough(**furlough_data)


@db_session
def create_visit(num_visits_per_prisoner=5):
    prisoner_ids = select(prisoner.id_prisoner for prisoner in Prisoner)[:]

    if len(prisoner_ids) == 0:
        raise Exception("No prisoners in database.")

    visits_count = int(len(prisoner_ids) * num_visits_per_prisoner)

    for visit in range(visits_count):
        start_date = fake.date_between(start_date=date(year=2020, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = time(hour=random.randint(8, 19), minute=random.randint(0, 59),
                          second=random.randint(0, 59))

        duration = timedelta(seconds=random.randint(15 * 60, 4 * 60 * 60))

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = start_datetime + duration

        visit_data = {
            'id_prisoner': random.choice(prisoner_ids),
            'start_date': start_datetime,
            'end_date': end_datetime,
            'name': fake.first_name(),
            'surname': fake.last_name()
        }

        Visit(**visit_data)


@db_session
def create_duties_with_guards(start_datetime=datetime(year=2023, month=1, day=1, hour=6, minute=0, second=0),
                              end_datetime=datetime(year=2023, month=6, day=30, hour=22, minute=0, second=0)):
    with db_session:
        blocks = Block.select()
        guards = Guard.select()
        prisons = Prison.select()

        if len(blocks) == 0:
            raise Exception("No blocks in database")

        if len(guards) == 0:
            raise Exception("No guards in database")

        if len(Duty.select()) != 0:
            raise Exception("Duties already created")

        duties_guards = []

        duration = timedelta(hours=8)

        prisons_guards = {prison: [guard for guard in prison.guards] for prison in prisons}
        prisons_blocks = {prison: [block for building in prison.buildings for block in building.blocks]
                          for prison in prisons}

        while start_datetime < end_datetime:
            for prison, p_blocks in prisons_blocks.items():
                if len(p_blocks) == 0:
                    continue

                duties = []
                for block in p_blocks:
                    duty_data = {
                        'block': block,
                        'start_date': start_datetime,
                        'end_date': start_datetime + duration
                    }

                    duties.append(Duty(**duty_data))

                available_guards = prisons_guards[prison]
                n = len(available_guards)

                if n < len(duties):
                    raise Exception("No guards available for duty")

                guards_on_duty_count = random.randint(0, n - len(duties))
                for duty in duties + random.choices(duties, k=guards_on_duty_count - len(duties)):
                    idx = random.randint(0, n - 1)
                    duties_guards.append((duty, available_guards[idx]))
                    available_guards[idx], available_guards[n - 1] = available_guards[n - 1], available_guards[idx]
                    n -= 1
            start_datetime += duration
    create_guard_duty(duties_guards)


@db_session
def create_guard_duty(duties_guards):
    for duty, guard in duties_guards:
        guard_duty_data = {
            'duty': duty,
            'guard': guard
        }
        GuardDuty(**guard_duty_data)


@db_session
def create_examinations(num_examinations_per_prisoner=5):
    prisoner_ids = select(prisoner.id_prisoner for prisoner in Prisoner)[:]
    doctor_ids = select(doctor.id_doctor for doctor in Doctor)[:]
    examination_types = ExaminationType.select()[:]

    if len(prisoner_ids) == 0:
        raise Exception("No prisoners in database.")

    if len(doctor_ids) == 0:
        raise Exception("No doctors in database.")

    if len(examination_types) == 0:
        raise Exception("No examination types in database.")

    examinations_count = int(len(prisoner_ids) * num_examinations_per_prisoner)

    for examination in range(examinations_count):
        doctor_id = random.choice(doctor_ids)
        prisoner_id = random.choice(prisoner_ids)
        examination_date = fake.date_time_between(start_date=datetime(year=2020, month=1, day=1),
                                                  end_date=datetime(year=2023, month=6, day=30))

        examination_type = random.choice(examination_types)
        result = EXAMINATIONS[examination_type.examination_type]

        examination_data = {
            'id_prisoner': prisoner_id,
            'examination_date': examination_date,
            'id_doctor': doctor_id,
            'id_examination_type': examination_type.id_examination_type,
            'examination_result': result()
        }

        Examination(**examination_data)


def create_guard(id_prison):
    rank_ids = select(r.id_rank for r in Rank)[:]

    if len(rank_ids) == 0:
        raise Exception("No Ranks in the database. Can't create a Guard.")

    pesel = fake.pesel()
    is_female = int(pesel[-2]) % 2 == 0
    if is_female:
        name = fake.first_name_female()
        surname = fake.last_name_female()
    else:
        name = fake.first_name_male()
        surname = fake.last_name_male()

    probability = 0.9
    guard_data = {
        'pesel': pesel,
        'name': name,
        'surname': surname,
        'id_prison': id_prison,
        'id_rank': random.choice(rank_ids) if random.random() < probability else None
    }

    Guard(**guard_data)


@db_session
def create_guards(num_mandatory_guards_per_block=5, num_additional_guards_per_block=10):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Guard.")

    prison_ids = [prison.id_prison for prison in prisons]
    guard_id = 1

    additional_guards_count = int(len(Block.select()) * num_additional_guards_per_block)
    for prison in prisons:
        for _ in range(num_mandatory_guards_per_block * sum(building.blocks.count() for building in prison.buildings)):
            create_guard(prison.id_prison)
            guard_id += 1
    for i in range(guard_id, guard_id + additional_guards_count):
        create_guard(random.choice(prison_ids))


def create_contact_persons(num_contact_persons):
    probability = 0.8
    contact_persons = deque()

    for i in range(num_contact_persons):
        contact_person_data = {
            'name': fake.first_name(),
            'surname': fake.last_name(),
            'phone_nr': fake.phone_number() if random.random() < probability else None,
            'kinship': random.choice(KINSHIPS) if random.random() < probability else None
        }

        contact_persons.append(ContactPerson(**contact_person_data))

    return contact_persons


def create_prisoners_with_sentences(num_prisoners_per_prison=300, has_contact_person_probability=0.8,
                                    sentences_count_weights=(0.5, 0.2, 0.15, 0.1, 0.05)):
    with db_session:
        prisons = Prison.select()

        if len(prisons) == 0:
            raise Exception("No Prisons in the database. Can't create a Prisoner.")

        cells = Cell.select()

        cells_capacity = {cell: cell.cell_capacity for cell in cells}
        cells_prisons = {cell: cell.id_block.id_building.id_prison.id_prison for cell in cells}
        available_male_cells = [cell for cell in cells if cell.id_cell_type.cell_type != 'Żeńska']
        available_female_cells = [cell for cell in cells if cell.id_cell_type.cell_type != 'Męska']

        prisoners_count = int(len(prisons) * num_prisoners_per_prison)

        contact_persons = create_contact_persons(int(prisoners_count * has_contact_person_probability))
    contact_persons += deque([None] * (prisoners_count - len(contact_persons)))
    random.shuffle(contact_persons)
    prisoners_sentences = []

    with db_session:
        for _ in range(prisoners_count):
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
            pesel = fake.pesel(date_of_birth=date_of_birth)
            sex_digit = int(pesel[-2])
            is_female = sex_digit % 2 == 0
            probability = 0.8
            if is_female:
                cell = random.choice(available_female_cells)
            else:
                cell = random.choice(available_male_cells)
            cells_capacity[cell] -= 1
            if cells_capacity[cell] == 0:
                with suppress(ValueError):
                    available_male_cells.remove(cell)
                with suppress(ValueError):
                    available_female_cells.remove(cell)

            sentences_count = random.choices(range(1, len(sentences_count_weights) + 1),
                                             weights=sentences_count_weights)[0]

            sentences = []
            for _ in range(sentences_count):
                # 9150 days is 25 years, more is life sentence, coded as 20 000
                duration = random.randint(1, 9200)
                if duration > 9150:
                    duration = 20000
                sentences.append(duration)

            sentence_time = sum(sentences)
            admission_date = fake.date_time_between(
                start_date=max(datetime.combine(date_of_birth + timedelta(days=365 * 17), time(hour=0, minute=0)),
                               datetime(year=2023, month=6, day=30) - timedelta(days=sentence_time)),
                end_date=datetime(year=2023, month=6, day=30)
            )

            prisoner_data = {
                'pesel': pesel,
                'first_name': fake.first_name_female() if is_female else fake.first_name_male(),
                'last_name': fake.last_name_female() if is_female else fake.last_name_male(),
                'admission_date': admission_date,
                'id_cell': cell.id_cell,
                'sex': 'F' if is_female else 'M',
                'blood_group': random.choice(BLOOD_GROUPS) if random.random() < probability else None,
                'id_prison': cells_prisons[cell]
            }

            if (contact := contact_persons.popleft()) is not None:
                prisoner_data['id_contact_person'] = contact.id_contact_person
            if random.random() < probability:
                prisoner_data['height'] = random.randint(150, 210)

            prisoner = Prisoner(**prisoner_data)
            prisoners_sentences.append((prisoner, sentences))

    create_sentences(prisoners_sentences)


@db_session
def create_sentences(prisoners_sentences):

    for prisoner, durations in prisoners_sentences:
        for duration in durations:
            sentence_data = {
                'id_prisoner': prisoner.id_prisoner,
                'stay_duration_days': duration,
                'article': str(random.randint(1, 400)),
                'paragraph': random.randint(1, 15)
            }

            Sentence(**sentence_data)


@db_session
def create_prisons(num_prisons=3):

    probability = 0.8
    for _ in range(num_prisons):
        prison_data = {
            'penitentiary_name': "Więzienie nr: " + str(random.randint(1, 100)),
            'city': fake.city(),
            'street': fake.street_name(),
            'building_nr': fake.building_number(),
            'apartment_nr': str(random.randint(1, 1000)) if random.random() < probability else None
        }

        Prison(**prison_data)


@db_session
def create_buildings(num_building_per_prison=5):
    prison_ids = select(p.id_prison for p in Prison)[:]

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
        Building(**building_data)


@db_session
def create_cells(num_cells_per_block=10):
    cell_types = CellType.select()[:]
    block_ids = select(block.id_block for block in Block)[:]

    if len(block_ids) == 0:
        raise Exception("No Blocks in the database. Can't create a Cell.")

    if len(cell_types) == 0:
        raise Exception("No CellTypes in the database. Can't create a Cell.")

    cells_count = int(len(block_ids) * num_cells_per_block)
    for i in range(cells_count):
        cell_type = random.choice(cell_types)
        cell_data = {
            'cell_nr': i,
            'id_cell_type': cell_type.id_cell_type,
            'cell_capacity': random.randint(1, 10) if cell_type != 'Izolacyjna' else 1,
            'id_block': random.choice(block_ids),
        }

        Cell(**cell_data)


@db_session
def create_cell_types():
    for cell_type_name in CELL_TYPES:
        CellType(cell_type=cell_type_name)


@db_session
def create_ranks():
    for rank in RANKS:
        Rank(rank=rank)


@db_session
def create_specializations():
    for specialization in SPECIALIZATIONS:
        Specialization(specialization=specialization)


@db_session
def create_blocks(num_blocks_per_prison=8):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Block.")

    buildings = Building.select()
    building_ids = [building.id_building for building in buildings]

    blocks_count = int(len(prisons) * num_blocks_per_prison)
    for i in range(blocks_count):
        block_data = {
            'block_name': random.choice(BLOCK_NAMES),
            'id_building': random.choice(building_ids),
        }

        Block(**block_data)


def populate_db():
    create_cell_types()
    create_specializations()
    create_ranks()
    create_examination_types()
    create_doctors()
    create_prisons()
    create_administrative_employees()
    create_buildings()
    create_blocks()
    create_cells()
    create_guards()
    create_users()
    create_prisoners_with_sentences()
    create_visit()
    create_examinations()
    create_furloughs()
    create_duties_with_guards()
