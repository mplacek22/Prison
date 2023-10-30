from datetime import date, timedelta
import random
from faker import *
from entities import *

fake = Faker("pl_PL")

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

EXAMINATIONS = [
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


@db_session
def create_administrative_employees(num_admins_per_prison=2000):
    # prison_ids = select(p.id_prison for p in Prison)[:]
    # if not prison_ids:
    #     raise Exception("No Prisons in the database. Can't create AdministrativeEmployee.")

    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create an AdministrativeEmployee.")

    prison_ids = [p.id_prison for p in prisons]

    admin_count = int(len(prisons) * num_admins_per_prison)
    for i in range(1, admin_count + 1):
        admin_data = {
            'id_employee': i,
            'pesel': fake.pesel(),
            'name': fake.first_name(),
            'surname': fake.last_name(),
            'id_prison': random.choice(prison_ids)
        }
        AdministrativeEmployee(**admin_data)


@db_session
def create_doctors(num_doctors=2000):
    for i in range(1, 1 + num_doctors):
        doctor_data = {
            'id_doctor': i,
            'pesel': fake.pesel(),
            'name': fake.first_name(),
            'surname': fake.last_name(),
            'specialization': random.choice(SPECIALIZATIONS)
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
def create_sentences(num_additional_sentences_per_prisoner=0.75):
    prisoners = list(Prisoner.select())

    if len(prisoners) == 0:
        print("No prisoners in database")
        return

    sentence_id = len(Sentence.select()) + 1
    additional_sentences = int(len(prisoners) * num_additional_sentences_per_prisoner)

    for prisoner in prisoners + random.choices(prisoners, k=additional_sentences):
        # 9150 days is 25 years, more is life sentence, coded as 20 000
        duration = random.randint(1, 9200)
        if duration > 9150:
            duration = 20000
        Sentence(id_sentence=sentence_id, prisoner=prisoner, stay_duration_days=duration,
                 article=str(random.randint(1, 400)), paragraph=random.randint(1, 15))

        sentence_id += 1


@db_session
def create_furloughs(num_furloughs_per_prisoner=2):
    prisoners = list(Prisoner.select())

    if len(prisoners) == 0:
        raise Exception("No prisoners in database")

    furlough_id = 0
    furloughs_count = int(len(prisoners) * num_furloughs_per_prisoner)

    for prisoner in random.choices(prisoners, k=furloughs_count):
        start_date = fake.date_between(start_date=date(year=2010, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = fake.time_object()

        end_time = fake.time_object()

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(start_date + timedelta(days=random.randint(1, 14)), end_time)

        Furlough(id_furlough=furlough_id, prisoner=prisoner,
                 start_date=start_datetime, end_date=end_datetime)

        furlough_id += 1


@db_session
def create_visit(num_visits_per_prisoner=5):
    prisoners = list(Prisoner.select())

    if len(prisoners) == 0:
        print("No prisoners in database.")
        return

    visit_id = len(Visit.select()) + 1
    visits_count = int(len(prisoners) * num_visits_per_prisoner)

    for prisoner in random.choices(prisoners, k=visits_count):
        start_date = fake.date_between(start_date=date(year=2010, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = fake.time_object()

        duration = timedelta(hours=random.randint(1, 3), minutes=random.randint(0, 59),
                             seconds=random.randint(0, 59))

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = start_datetime + duration

        Visit(id_visit=visit_id, prisoner=prisoner, start_date=start_datetime, end_date=end_datetime,
              name=fake.first_name(), surname=fake.last_name())

        visit_id += 1


@db_session
def create_duties_with_guards(start_datetime=datetime(year=2023, month=6, day=1, hour=6, minute=0, second=0),
                              end_datetime=datetime(year=2023, month=6, day=30, hour=22, minute=0, second=0)):
    blocks = Block.select()
    guards = Guard.select()

    if len(blocks) == 0:
        print("No blocks in database")
        return

    if len(guards) == 0:
        print("No guards in database")
        return

    if len(Duty.select()) != 0:
        print("Duties already created")
        return

    duty_id = 0
    duration = timedelta(hours=8)

    while start_datetime < end_datetime:
        busy_guards = set()
        for block in blocks:
            duty = Duty(id_duty=duty_id, block=block, start_date=start_datetime, end_date=start_datetime + duration)
            db.flush()
            available_guards = list(guards.filter(
                lambda g: g.id_prison == block.id_building.id_prison and g not in busy_guards))

            # if len(available_guards) == 0:
            #     raise Exception("No guards available for duty")

            for guard in random.sample(available_guards, k=min(random.randint(1, 5), len(available_guards))):
                GuardDuty(duty=duty, guard=guard)
                busy_guards.add(guard)
            duty_id += 1
        start_datetime += duration


@db_session
def create_examinations(num_examinations_per_prisoner=5):
    prisoners = list(Prisoner.select())
    doctors = list(Doctor.select())

    if len(prisoners) == 0:
        print("No prisoners in database.")
        return

    examination_id = len(Examination.select()) + 1
    examinations_count = int(len(prisoners) * num_examinations_per_prisoner)

    for prisoner in random.choices(prisoners, k=examinations_count):
        doctor = random.choice(doctors)
        examination_date = fake.date_time_between(start_date=datetime(year=2010, month=1, day=1),
                                                  end_date=datetime(year=2023, month=6, day=30))

        name, result = random.choice(EXAMINATIONS)

        Examination(id_examination=examination_id, prisoner=prisoner, examination_date=examination_date,
                    doctor=doctor, examination_type=name, examination_result=result())

        examination_id += 1


@db_session
def create_guards(num_guards_per_block=20):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Guard.")

    prison_ids = [prison.id_prison for prison in prisons]

    guards_count = int(len(Block.select()) * num_guards_per_block)
    for i in range(1, 1 + guards_count):
        guard_data = {
            'id_guard': i,
            'pesel': fake.pesel(),
            'name': fake.first_name(),
            'surname': fake.last_name(),
            'id_prison': random.choice(prison_ids)
        }

        probability = 0.8
        if random.random() < probability:
            guard_data['rank'] = str(random.randint(1, 100))

        Guard(**guard_data)


@db_session
def create_contact_persons(num_contact_persons_per_prisoner=1):
    prisoners = Prisoner.select()

    contact_persons_count = int(len(prisoners) * num_contact_persons_per_prisoner)
    for i in range(1, 1 + contact_persons_count):
        contact_person_data = {
            'id_contact_person': i,
            'name': fake.first_name(),
            'surname': fake.last_name(),
        }

        probability = 0.8
        if random.random() < probability:
            contact_person_data['phone_nr'] = fake.phone_number()
        if random.random() < probability:
            contact_person_data['kinship'] = random.choice(KINSHIPS)

        ContactPerson(**contact_person_data)


@db_session
def create_prisoners(num_prisoners_per_prison=2000):
    prisons = Prison.select()

    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Prisoner.")

    cells = Cell.select()
    cell_ids = [cell.id_cell for cell in cells]

    contact_persons = ContactPerson.select()
    contact_person_ids = [person.id_contact_person for person in contact_persons]

    prisoners_count = int(len(prisons) * num_prisoners_per_prison)
    start_id = len(Prisoner.select()) + 1
    for i in range(start_id, start_id + prisoners_count):

        pesel = fake.pesel()
        last_digit = int(pesel[-1])
        probability = 0.8

        prisoner_data = {
            'id_prisoner': i,
            'pesel': pesel,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'admission_date': fake.date_time_between(start_date=datetime(year=1960, month=1, day=1),
                                                     end_date=datetime(year=2023, month=6, day=30)),
            'id_cell': random.choice(cell_ids),
            'sex': 'F' if last_digit % 2 == 0 else 'M',
            'blood_group': random.choice(BLOOD_GROUPS) if random.random() < probability else ''
        }

        if random.random() < probability:
            prisoner_data['id_contact_person'] = random.choice(contact_person_ids)
        if random.random() < probability:
            prisoner_data['height'] = random.randint(150, 210)

        Prisoner(**prisoner_data)


@db_session
def create_prisons(num_prisons=50):
    prisons = Prison.select()

    probability = 0.8
    start_id = len(prisons) + 1
    for i in range(start_id, start_id + num_prisons):
        prison_data = {
            'id_prison': i,
            'penitentiary_name': f'Prison nr: {i}',
            'city': fake.city(),
            'street': fake.street_name(),
            'building_nr': fake.building_number(),
            'apartment_nr': str(random.randint(1, 1000)) if random.random() < probability else ''
        }

        Prison(**prison_data)


@db_session
def create_buildings(num_buildings_per_prison=100):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Building.")

    prison_ids = [prison.id_prison for prison in prisons]

    buildings_count = int(len(prisons) * num_buildings_per_prison)
    start_id = len(Building.select()) + 1
    for i in range(1, start_id + buildings_count):
        building_data = {
            'id_building': i,
            'city': fake.city(),
            'street': fake.street_address(),
            'building_nr': str(random.randint(1, 50)),
            'id_prison': random.choice(prison_ids)
        }

        Building(**building_data)


@db_session
def create_cells(num_cells_per_block=1000):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Cell.")

    cell_types = CellType.select()
    cell_type_ids = [cell_type.id_cell_type for cell_type in cell_types]

    blocks = Block.select()
    block_ids = [block.id_block for block in blocks]

    cells_count = int(len(blocks) * num_cells_per_block)
    start_id = len(Cell.select()) + 1
    for i in range(start_id, start_id + cells_count):
        cell_data = {
            'id_cell': i,
            'cell_nr': i,
            'id_cell_type': random.choice(cell_type_ids),
            'cell_capacity': random.randint(1, 10),
            'id_block': random.choice(block_ids),
        }

        Cell(**cell_data)


@db_session
def create_cell_types():
    cell_type = {
        1: 'male',
        2: 'female',
        3: 'separate'
    }

    for cell_type_id, cell_type_name in cell_type.items():
        if not select(c for c in CellType if c.id_cell_type == cell_type_id).exists():
            CellType(id_cell_type=cell_type_id, cell_type=cell_type_name)


@db_session
def create_blocks(num_blocks_per_prison=100):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Block.")

    buildings = Building.select()
    building_ids = [building.id_building for building in buildings]

    blocks_count = int(len(prisons) * num_blocks_per_prison)
    start_id = len(Block.select()) + 1
    for i in range(start_id, start_id + blocks_count):
        block_data = {
            'id_block': i,
            'block_name': random.choice(BLOCK_NAMES),
            'id_building': random.choice(building_ids),
        }

        Block(**block_data)


def populate_db():
    create_cell_types()
    create_contact_persons()
    create_doctors()
    create_prisons()
    create_administrative_employees()
    create_buildings()
    create_blocks()
    create_cells()
    create_guards()
    create_users()
    create_prisoners()
    create_sentences()
    create_visit()
    create_examinations()
    create_furloughs()
    create_duties_with_guards()
