from datetime import datetime
from pony.orm import *

db = Database()


# Define the "CellType" entity
class CellType(db.Entity):
    id_cell_type = PrimaryKey(int, column="IdCellType")
    cell_type = Required(str, column="CellType")


# Define the "ContactPerson" entity
class ContactPerson(db.Entity):
    id_contact_person = PrimaryKey(int, column="IdContactPerson")
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    kinship = Optional(str, column="Kinship")
    phone_nr = Optional(str, column="PhoneNr")


# Define the "Doctor" entity
class Doctor(db.Entity):
    id_doctor = PrimaryKey(int, column="IdDoctor")
    pesel = Required(str, column="PESEL")
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    specialization = Required(str, column="Specialization")


# Define the "Prison" entity
class Prison(db.Entity):
    id_penitentiary = PrimaryKey(int, column="IdPenitentiary")
    penitentiary_name = Required(str, column="PenitentiaryName")
    city = Required(str, column="City")
    street = Required(str, column="Street")
    building_nr = Required(str, column="BuildingNr")
    apartment_nr = Required(str, column="ApartmentNr")


# Define the "AdministrativeEmployee" entity
class AdministrativeEmployee(db.Entity):
    id_employee = PrimaryKey(int, column="IdEmployee")
    pesel = Required(str, column="PESEL", check=lambda val: len(val) == 11)
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    id_penitentiary = Required(Prison, column="IdPenitentiary")


# Define the "Building" entity
class Building(db.Entity):
    id_building = PrimaryKey(int, column="IdBuilding")
    city = Required(str, column="City")
    street = Required(str, column="Street")
    building_nr = Required(str, column="BuildingNr")
    id_penitentiary = Required(Prison, column="IdPenitentiary")


# Define the "Guard" entity
class Guard(db.Entity):
    id_guard = PrimaryKey(int, column="IdGuard")
    pesel = Required(str, column="PESEL", check=lambda val: len(val) == 11)
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    rank = Optional(str, column="Rank")
    id_penitentiary = Required(Prison, column="IdPenitentiary")


# Define the "User" entity
class User(db.Entity):
    username = PrimaryKey(str, column="Username")
    password = Required(int, column="Password")
    id_employee = Optional(AdministrativeEmployee, column="IdEmployee")
    id_guard = Optional(Guard, column="IdGuard")
    id_doctor = Optional(Doctor, column="IdDoctor")
    # check(lambda: (id_doctor is not None) + (id_guard is not None) + (id_employee is not None) == 1)


# Define the "Block" entity
class Block(db.Entity):
    id_block = PrimaryKey(int, column="IdBlok")
    block_name = Required(str, column="BlockName")
    id_building = Required(Building, column="IdBuilding")


# Define the "Cell" entity
class Cell(db.Entity):
    id_cell = PrimaryKey(int, column="IdCell")
    cell_nr = Required(int, column="CellNr")
    id_cell_type = Required(CellType, column="IdCellType")
    cell_capacity = Required(int, column="CellCapacity", check=lambda val: val > 0)
    id_block = Required(Block, column="IdBlock")


# Define the "Duty" entity
class Duty(db.Entity):
    id_duty = PrimaryKey(int, column="IdDuty")
    start_date = Required(datetime, column="StartDate")
    end_date = Required(datetime, column="EndDate")  # , check=lambda val: val > start_date)
    id_block = Required(Block, column="IdBlock")


# Define the "GuardDuty" entity
class GuardDuty(db.Entity):
    id_duty = Required(Duty, column="IdDuty")
    id_guard = Required(Guard, column="IdGuard")


# Define the blood group enum
class BloodGroupEnum(db.Entity):
    value = Required(str, column="value")


# Define the sex enum
class SexEnum(db.Entity):
    value = Required(str, column="value")


# Define the "Prisoner" entity
class Prisoner(db.Entity):
    id_prisoner = PrimaryKey(int, column="IdPrisoner")
    pesel = Required(str, column="PESEL", check=lambda val: len(val) == 11)
    first_name = Required(str, column="FirstName")
    last_name = Required(str, column="LastName")
    admission_date = Required(datetime, column="AdmissionDate")
    id_cell = Required(Cell, column="IdCell")
    id_contact_person = Optional(ContactPerson, column="IdContactPerson")
    height = Optional(float, column="Height", check=lambda val: val > 0)
    blood_group = Optional(BloodGroupEnum, column="BloodGroup")
    sex = Required(SexEnum, column="Sex")


# Define the "Sentence" entity
class Sentence(db.Entity):
    id_sentence = PrimaryKey(int, column="IdSentence")
    article = Required(str, column="Article")
    paragraph = Required(int, column="Paragraph")
    stay_duration_days = Required(int, column="StayDurationDays", check=lambda val: val > 0)
    id_prisoner = Required(Prisoner, column="IdPrisoner")


# Define the "Visit" entity
class Visit(db.Entity):
    id_pass = PrimaryKey(int, column="IdPass")
    id_prisoner = Required(Prisoner, column="IdPrisoner")
    start_date = Required(datetime, column="StartDate")
    end_date = Required(datetime, column="EndDate")  # , check=lambda val: val > start_date)
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")


# Define the "Examination" entity
class Examination(db.Entity):
    id_examination = PrimaryKey(int, column="IdExamination")
    id_doctor = Required(Doctor, column="IdDoctor")
    id_prisoner = Required(Prisoner, column="IdPrisoner")
    examination_type = Required(str, column="ExaminationType")
    examination_date = Required(datetime, column="ExaminationDate")
    examination_result = Required(str, column="ExaminationResult")
