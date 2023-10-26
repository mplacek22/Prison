import random
from datetime import date, timedelta

from faker import Faker

from entities import *

fake = Faker()


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
        print("No prisoners in database")
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
        print("No prisoners in database")
        return

    examination_id = 0
    examinations_count = int(len(prisoners) * 5)

    examinations = [
        ("MAsa ciała", lambda: str(round(random.uniform(40.0, 150.0), 1)) + " kg"),
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

    for prisoner in random.choices(prisoners, k=examinations_count):
        doctor = random.choice(doctors)
        examination_date = fake.date_time_between(start_date=datetime(year=2010, month=1, day=1),
                                                  end_date=datetime(year=2023, month=6, day=30))

        name, result = random.choice(examinations)

        examination = Examination(id_examination=examination_id, prisoner=prisoner, examination_date=examination_date,
                                  doctor=doctor, examination_type=name, examination_result=result)

        examination_id += 1