from datetime import date, timedelta
import random
from faker import *
from random_pesel import RandomPESEL
from entities import *

fake = Faker()
pesel = RandomPESEL()


@db_session
def create_administrative_employees(num_admins):
    if count(Prison) == 0:
        raise Exception("No Prisons in the database. Can't create AdministrativeEmployee.")

    start_id = count(AdministrativeEmployee) + 1
    prisons = select(p for p in Prison)

    for i in range(start_id, start_id + num_admins):
        admin_data = {
            'id_employee': i,
            'pesel': str(pesel.generate()),
            'name': fake.first_name(),
            'surname': fake.last_name(),
            'id_prison': random.choice(prisons)
        }
        AdministrativeEmployee(**admin_data)


@db_session
def create_doctors(num_doctors):
    specializations = [
        "Cardiologist",
        "Pediatrician",
        "Neurologist",
        "Dermatologist",
        "Orthopedic Surgeon",
        "Gynecologist",
        "Gastroenterologist",
        "Radiologist",
        "Ophthalmologist",
        "Urologist",
        "Oncologist",
        "Pulmonologist",
        "Endocrinologist",
        "Nephrologist",
        "Rheumatologist",
        "Psychiatrist",
        "Anesthesiologist",
        "General Surgeon",
        "Infectious Disease Specialist",
        "Hematologist"
    ]
    start_id = count(d for d in Doctor) + 1
    for i in range(start_id, start_id + num_doctors):
        Doctor(id_doctor=i, pesel=str(pesel.generate()), name=fake.first_name(), surname=fake.last_name(),
               specialization=random.choice(specializations))


@db_session
def create_users():
    for admin in AdministrativeEmployee.select():
        User(username=fake.unique.username(), password=fake.password(length=random.randint(8, 30)),
             id_employee=admin.id_employee)
    for guard in Guard.select():
        User(username=fake.unique.username(), password=fake.password(), id_guard=guard.id_guard)
    for doctor in Doctor.select():
        User(username=fake.unique.user_name(), password=fake.password(), id_doctor=doctor.id_doctor)


@db_session
def create_sentences():
    prisoners = Prisoner.select()

    if len(prisoners) == 0:
        print("No prisoners in database")
        return

    sentence_id = 0
    additional_sentences = int(len(prisoners) * 0.75)

    for prisoner in prisoners + random.choices(prisoners, k=additional_sentences):
        # 9150 days is 25 years, more is life sentence, coded as 20 000
        duration = random.randint(1, 9200)
        if duration > 9150:
            duration = 20000
        sentence = Sentence(id_sentence=sentence_id, prisoner=prisoner,
                            stay_duration_days=duration, article=str(random.randint(1, 400)),
                            paragraph=random.randint(1, 15))

        sentence_id += 1


@db_session
def create_furloughs():
    prisoners = Prisoner.select()

    if len(prisoners) == 0:
        print("No prisoners in database")
        return

    furlough_id = 0
    furloughs_count = int(len(prisoners) * 2)

    for prisoner in random.choices(prisoners, k=furloughs_count):
        start_date = fake.date_between(start_date=date(year=2010, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = fake.time_object(end_datetime=datetime(year=2010, month=1, day=1, hour=18, minute=0, second=0),
                                      timedelta=timedelta(hours=10))

        end_time = fake.time_object(end_datetime=datetime(year=2010, month=1, day=1, hour=18, minute=0, second=0),
                                    timedelta=timedelta(hours=10))

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(start_date + timedelta(days=random.randint(1, 14)), end_time)

        furlough = Furlough(id_furlough=furlough_id, prisoner=prisoner,
                            start_date=start_datetime, end_date=end_datetime)

        furlough_id += 1


@db_session
def create_visit():
    prisoners = Prisoner.select()

    if len(prisoners) == 0:
        print("No prisoners in database.")
        return

    visit_id = 0
    visits_count = int(len(prisoners) * 5)

    for prisoner in random.choices(prisoners, k=visits_count):
        start_date = fake.date_between(start_date=date(year=2010, month=1, day=1),
                                       end_date=date(year=2023, month=6, day=30))
        start_time = fake.time_object(end_datetime=datetime(year=2010, month=1, day=1, hour=18),
                                      timedelta=timedelta(hours=10))

        duration = fake.time_delta("+3h")

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = start_datetime + duration

        visit = Visit(id_visit=visit_id, id_prisoner=prisoner,
                      start_date=start_datetime, end_date=end_datetime,
                      name=fake.first_name(), surname=fake.last_name())

        visit_id += 1


@db_session
def create_duties():
    blocks = Block.select()

    if len(blocks) == 0:
        print("No blocks in database")
        return

    duty_id = 0
    start_datetime = datetime(year=2010, month=1, day=1, hour=6, minute=0, second=0)
    duration = timedelta(hours=8)

    while start_datetime <= datetime(year=2023, month=6, day=30, hour=22, minute=0, second=0):
        for block in blocks:
            duty = Duty(id_duty=duty_id, block=block, start_date=start_datetime, end_date=start_datetime + duration)
            duty_id += 1
        start_datetime += timedelta(days=1)


@db_session
def create_guard_duties():
    guards = Guard.select()
    duties = Duty.select()

    if len(guards) == 0:
        print("No guards in database")
        return
    if len(duties) == 0:
        print("No duties in database")
        return

    busy_guards = set()

    for duty in duties:
        available_guards = guards.filter(
            lambda guard: guard.id_penitentiary == duty.id_block.id_building.id_penitentiary
                          and guard not in busy_guards)

        if len(available_guards) == 0:
            print("No guards available for duty")
            return

        for guard in random.choices(available_guards, k=random.randint(1, 5)):
            guard_duty = GuardDuty(duty=duty, guard=guard)
            busy_guards.add(guard)


@db_session
def create_examinations():
    prisoners = Prisoner.select()
    doctors = Doctor.select()

    if len(prisoners) == 0:
        print("No prisoners in database.")
        return

    examination_id = 0
    examinations_count = int(len(prisoners) * 5)

    # examinations = [
    #     ("MAsa ciała", lambda: str(round(random.uniform(40.0, 150.0), 1)) + " kg"),
    #     ("Temperatura ciała", lambda: str(round(random.uniform(36.0, 41.0), 1)) + " °C"),
    #     ("Poziom cukru we krwi", lambda: str(round(random.uniform(70, 120), 1))),
    #     ("Ciśnienie krwi", lambda: str(random.randint(90, 180)) + "/" + str(random.randint(60, 130)) + " mmHg"),
    #     ("Poziom cholesterolu", lambda: random.choice(["Wynik prawidłowy", "Podwyższony", "Zbyt niski"])),
    #     ("Wynik morfologii krwi", lambda: random.choice(["Normalny", "Anemia", "Leukocytoza"])),
    #     ("Poziom wapnia we krwi", lambda: str(round(random.uniform(8.0, 10.5), 2))),
    #     ("Poziom potasu we krwi", lambda: str(round(random.uniform(3.5, 5.5), 2))),
    #     ("Poziom sodu we krwi", lambda: str(round(random.uniform(135, 145), 2))),
    #     ("Wynik testu alergii", lambda: random.choice(["Brak alergii", "Alergia na pyłki", "Alergia na orzechy"])),
    #     ("Poziom witaminy D", lambda: str(round(random.uniform(20, 60), 2))),
    #     ("Poziom magnezu we krwi", lambda: str(round(random.uniform(1.5, 2.5), 2))),
    #     ("Poziom cynku we krwi", lambda: str(round(random.uniform(50, 120), 2))),
    #     ("Wynik prób wątrobowych",
    #      lambda: random.choice(["Wynik prawidłowy", "Podwyższone", "Podejrzenie uszkodzenia wątroby"])),
    #     ("Poziom trójglicerydów", lambda: str(round(random.uniform(50, 200), 1))),
    #     ("Poziom kreatyniny we krwi", lambda: str(round(random.uniform(0.5, 1.5), 2))),
    #     ("Kolonoskopia", lambda: random.choice(["Wynik negatywny", "Polip wykryty", "Nowotwór wykryty"])),
    #     ("Mammografia", lambda: random.choice(["Wynik negatywny", "Znaleziono nieprawidłowość"])),
    #     ("USG jamy brzusznej", lambda: random.choice(["Wynik prawidłowy", "Znaleziono nieprawidłowość"])),
    #     ("Elektrokardiogram", lambda: random.choice(["Wynik prawidłowy", "Zaburzenia rytmu", "Niedokrwienie serca"])),
    #     ("Konsultacja okulisty", lambda: random.choice(["Wynik prawidłowy", "Wymagana dalsza konsultacja"])),
    #     ("Badanie moczu", lambda: random.choice(["Wynik prawidłowy", "Obecność infekcji", "Inne nieprawidłowości"])),
    #     ("Test COVID-19", lambda: random.choice(["Wynik negatywny", "Wynik pozytywny", "Wymagane dalsze testy"]))
    # ]
    examinations = [
        ("Body Weight", lambda: str(round(random.uniform(40.0, 150.0), 1)) + " kg"),
        ("Body Temperature", lambda: str(round(random.uniform(36.0, 41.0), 1)) + " °C"),
        ("Blood Sugar Level", lambda: str(round(random.uniform(70, 120), 1))),
        ("Blood Pressure", lambda: str(random.randint(90, 180)) + "/" + str(random.randint(60, 130)) + " mmHg"),
        ("Cholesterol Level", lambda: random.choice(["Normal result", "Elevated", "Too low"])),
        ("Blood Morphology Result", lambda: random.choice(["Normal", "Anemia", "Leukocytosis"])),
        ("Calcium Level in Blood", lambda: str(round(random.uniform(8.0, 10.5), 2))),
        ("Potassium Level in Blood", lambda: str(round(random.uniform(3.5, 5.5), 2))),
        ("Sodium Level in Blood", lambda: str(round(random.uniform(135, 145), 2))),
        ("Allergy Test Result", lambda: random.choice(["No allergy", "Pollen allergy", "Nut allergy"])),
        ("Vitamin D Level", lambda: str(round(random.uniform(20, 60), 2))),
        ("Magnesium Level in Blood", lambda: str(round(random.uniform(1.5, 2.5), 2))),
        ("Zinc Level in Blood", lambda: str(round(random.uniform(50, 120), 2))),
        ("Liver Function Test Result", lambda: random.choice(["Normal result", "Elevated", "Suspected liver damage"])),
        ("Triglyceride Level", lambda: str(round(random.uniform(50, 200), 1))),
        ("Creatinine Level in Blood", lambda: str(round(random.uniform(0.5, 1.5), 2))),
        ("Colonoscopy", lambda: random.choice(["Negative result", "Polyp detected", "Tumor detected"])),
        ("Mammography", lambda: random.choice(["Negative result", "Abnormality detected"])),
        ("Abdominal Ultrasound", lambda: random.choice(["Normal result", "Abnormality detected"])),
        ("Electrocardiogram", lambda: random.choice(["Normal result", "Rhythm disturbances", "Heart ischemia"])),
        ("Ophthalmologist Consultation", lambda: random.choice(["Normal result", "Further consultation required"])),
        ("Urine Test", lambda: random.choice(["Normal result", "Presence of infection", "Other abnormalities"])),
        ("COVID-19 Test", lambda: random.choice(["Negative result", "Positive result", "Further testing required"]))
    ]

    for prisoner in random.choices(prisoners, k=examinations_count):
        doctor = random.choice(doctors)
        examination_date = fake.date_time_between(start_date=datetime(year=2010, month=1, day=1),
                                                  end_date=datetime(year=2023, month=6, day=30))

        name, result = random.choice(examinations)

        examination = Examination(id_examination=examination_id, prisoner=prisoner, examination_date=examination_date,
                                  doctor=doctor, examination_type=name, examination_result=result)

        examination_id += 1


@db_session
def create_guard(num_guards):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Guard.")

    start_id = len(Guard.select()) + 1
    prison_ids = [prison.id_penitentiary for prison in prisons]

    for i in range(start_id, start_id + num_guards):
        guard_data = {
            'id_guard': i,
            'pesel': str(pesel.generate()),
            'name': fake.first_name(),
            'surname': fake.last_name(),
            'id_penitentiary': random.choice(prison_ids)
        }

        # Conditionally add 'rank' attribute with a random value
        if random.choice([True, False]):
            guard_data['rank'] = str(random.randint(1, 100))  # nie pamiętam o co chodziło z tym rank

        Guard(**guard_data)


@db_session
def create_contact_person(num_contact_person):
    prisoners = Prisoner.select()

    # if len(prisoners) == 0:
    #     raise Exception("No prisoners in the database. Can't create a Contact person.")

    start_id = len(ContactPerson.select()) + 1
    kinships = [
        "Parent",
        "Grandparent",
        "Child",
        "Grandchild",
        "Sibling",
        "Spouse",
        "Relative",
        "Acquaintance",
        "Stranger",
    ]

    for i in range(start_id, start_id + num_contact_person):
        contact_person_data = {
            'id_contact_person': i,
            'name': fake.first_name(),
            'surname': fake.last_name(),
        }

        # Conditionally add 'kinship' and 'phone_nr' attributes with a random value
        if random.choice([True, False]):
            contact_person_data['phone_nr'] = fake.phone_number()
        if random.choice([True, False]):
            contact_person_data['kinship'] = random.choice(kinships)

        ContactPerson(**contact_person_data)


@db_session
def create_prisoner(num_prisoner):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Prisoner.")

    genders = ['F', 'M']
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', '0+', '0-']

    cells = Cell.select()
    cell_ids = [cell.id_cell for cell in cells]

    contact_persons = ContactPerson.select()
    contact_person_ids = [person.id_contact_person for person in contact_persons]

    start_id = len(Prisoner.select()) + 1
    for i in range(start_id, start_id + num_prisoner):
        prisoner_data = {
            'id_prisoner': i,
            'pesel': str(pesel.generate()),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'admission_date': fake.date_time_between(start_date=datetime(year=1960, month=1, day=1),
                                                     end_date=datetime(year=2023, month=6, day=30)),
            'id_cell': random.choice(cell_ids),
            'sex': random.choice(genders)
        }

        if random.choice([True, False]):
            prisoner_data['id_contact_person'] = random.choice(contact_person_ids)
        if random.choice([True, False]):
            prisoner_data['height'] = random.randint(150, 210)
        if random.choice([True, False]):
            prisoner_data['blood_group'] = random.choice(blood_groups)
        else:
            prisoner_data['blood_group'] = ''

        Prisoner(**prisoner_data)


@db_session
def create_prison(num_prison):
    prisons = Prison.select()
    if len(prisons) == 0:
        print("No Prisons in the database yet.")

    start_id = len(prisons) + 1
    for i in range(start_id, start_id + num_prison):
        prison_data = {
            'id_penitentiary': i,
            'penitentiary_name': f'Penitentiary nr: {i}',
            'city': fake.city(),
            'street': fake.street_address(),
            'building_nr': str(random.randint(1, 50))
        }

        if random.choice([True, False]):
            prison_data['apartment_nr'] = str(random.randint(1, 50))  # tu też nie pamiętam o co chodzi

        Prison(**prison_data)


@db_session
def create_building(num_building):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Building.")

    prison_ids = [prison.id_penitentiary for prison in prisons]

    start_id = len(Building.select()) + 1
    for i in range(start_id, start_id + num_building):
        building_data = {
            'id_building': i,
            'city': fake.city(),
            'street': fake.street_address(),
            'building_nr': str(random.randint(1, 50)),
            'id_penitentiary': random.choice(prison_ids)
        }

        Building(**building_data)


@db_session
def create_cell(num_cell):
    prisons = Prison.select()
    if len(prisons) == 0:
        raise Exception("No Prisons in the database. Can't create a Cell.")

    cell_types = CellType.select()
    cell_type_ids = [cell_type.id_cell_type for cell_type in cell_types]

    blocks = Block.select()
    block_ids = [block.id_block for block in blocks]

    start_id = len(Cell.select()) + 1
    for i in range(start_id, start_id + num_cell):
        cell_data = {
            'id_cell': i,
            'cell_nr': i,
            'id_cell_type': random.choice(cell_type_ids),
            'cell_capacity': random.randint(1, 10),
            'id_block': random.choice(block_ids),
        }

        Cell(**cell_data)


# @db_session
# def create_cell_type():
#     cell_type = {
#         '1': 'male',
#         '2': 'female',
#         '3': 'separate'
#     }
#
#     for cell_type_id, cell_type_name in cell_type.items():
#         CellType(id_cell_type=cell_type_id, cell_type=cell_type_name)

@db_session
def create_cell_type():
    cell_type = {
        '1': 'male',
        '2': 'female',
        '3': 'separate'
    }

    for cell_type_id, cell_type_name in cell_type.items():
        if not select(c for c in CellType if c.id_cell_type == cell_type_id).exists():
            CellType(id_cell_type=cell_type_id, cell_type=cell_type_name)

# @db_session
# def create_cell_type(num_cell_type):
#     cell_type = ['male', 'female', 'separate']
#
#     start_id = len(CellType.select()) + 1
#     for i in range(start_id, start_id + num_cell_type):
#         cell_type_data = {
#             'id_cell_type': i,
#             'cell_type': random.choice(cell_type),
#         }
#
#         CellType(**cell_type_data)


@db_session
def create_block(num_block):
    buildings = Building.select()
    if len(buildings) == 0:
        raise Exception("No Buildings in the database. Can't create a Block.")

    building_ids = [building.id_building for building in buildings]

    block_names = [
        'Separated',
        'Minor',
        'Min Security',
        'Max Security',
        'Mental illnesses',
        'Community work'
    ]

    start_id = len(Block.select()) + 1
    for i in range(start_id, start_id + num_block):
        block_data = {
            'id_block': i,
            'block_name': random.choice(block_names),
            'id_building': random.choice(building_ids),
        }

        Block(**block_data)
