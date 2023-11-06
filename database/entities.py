from datetime import datetime
from pony.orm import *

db = Database()


# Define the "CellType" entity
class CellType(db.Entity):
    _table_ = "CellType"
    id_cell_type = PrimaryKey(int, column="IdCellType", auto=True)
    cell_type = Required(str, column="CellType")
    cells = Set("Cell")


# Define the "Rank" entity
class Rank(db.Entity):
    _table_ = "Rank"
    id_rank = PrimaryKey(int, column="IdRank", auto=True)
    rank = Required(str, column="Rank")
    guards = Set("Guard")


# Define the "Specialization" entity
class Specialization(db.Entity):
    _table_ = "Specialization"
    id_specialization = PrimaryKey(int, column="IdSpecialization", auto=True)
    specialization = Required(str, column="Specialization")
    doctors = Set("Doctor")


# Define the "ContactPerson" entity
class ContactPerson(db.Entity):
    _table_ = "ContactPerson"
    id_contact_person = PrimaryKey(int, column="IdContactPerson", auto=True)
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    kinship = Optional(str, column="Kinship", nullable=True)
    phone_nr = Optional(str, column="PhoneNr", nullable=True)
    prisoners = Set("Prisoner")


# Define the "Doctor" entity
class Doctor(db.Entity):
    _table_ = "Doctor"
    id_doctor = PrimaryKey(int, column="IdDoctor", auto=True)
    pesel = Required(str, column="PESEL")
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    id_specialization = Required(Specialization, column="IdSpecialization")
    users = Set("User")
    examinations = Set("Examination")


# Define the "Prison" entity
class Prison(db.Entity):
    _table_ = "Prison"
    id_prison = PrimaryKey(int, column="IdPrison", auto=True)
    penitentiary_name = Required(str, column="PenitentiaryName")
    city = Required(str, column="City")
    street = Required(str, column="Street")
    building_nr = Required(str, column="BuildingNr")
    apartment_nr = Optional(str, column="ApartmentNr", nullable=True)
    administrative_employees = Set("AdministrativeEmployee")
    buildings = Set("Building")
    guards = Set("Guard")
    prisoners = Set("Prisoner")


# Define the "AdministrativeEmployee" entity
class AdministrativeEmployee(db.Entity):
    _table_ = "AdministrativeEmployee"
    id_employee = PrimaryKey(int, column="IdEmployee", auto=True)
    pesel = Required(str, column="PESEL")
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    id_prison = Required(Prison, column="IdPrison")
    users = Set("User")


# Define the "Building" entity
class Building(db.Entity):
    _table_ = "Building"
    id_building = PrimaryKey(int, column="IdBuilding", auto=True)
    city = Required(str, column="City")
    street = Required(str, column="Street")
    building_nr = Required(str, column="BuildingNr")
    id_prison = Required(Prison, column="IdPrison")
    blocks = Set("Block")


# Define the "Guard" entity
class Guard(db.Entity):
    _table_ = "Guard"
    id_guard = PrimaryKey(int, column="IdGuard", auto=True)
    pesel = Required(str, column="PESEL")
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")
    id_rank = Optional(Rank, column="IdRank")
    id_prison = Required(Prison, column="IdPrison")
    users = Set("User")
    duties = Set("GuardDuty")


# Define the "User" entity
class User(db.Entity):
    _table_ = "User"
    username = PrimaryKey(str, column="Username")
    password = Required(str, column="Password")
    id_employee = Optional(AdministrativeEmployee, column="IdEmployee", reverse="users")
    id_guard = Optional(Guard, column="IdGuard", reverse="users")
    id_doctor = Optional(Doctor, column="IdDoctor", reverse="users")


# Define the "Block" entity
class Block(db.Entity):
    _table_ = "Block"
    id_block = PrimaryKey(int, column="IdBlock", auto=True)
    block_name = Required(str, column="BlockName")
    id_building = Required(Building, column="IdBuilding")
    cells = Set("Cell")
    duties = Set("Duty")


# Define the "Cell" entity
class Cell(db.Entity):
    _table_ = "Cell"
    id_cell = PrimaryKey(int, column="IdCell", auto=True)
    cell_nr = Required(int, column="CellNr")
    id_cell_type = Required(CellType, column="IdCellType")
    cell_capacity = Required(int, column="CellCapacity")
    id_block = Required(Block, column="IdBlock")
    prisoners = Set("Prisoner")


# Define the "Duty" entity
class Duty(db.Entity):
    _table_ = "Duty"
    id_duty = PrimaryKey(int, column="IdDuty", auto=True)
    start_date = Required(datetime, column="StartDate")
    end_date = Required(datetime, column="EndDate")  # , check=lambda val: val > start_date)
    block = Required(Block, column="IdBlock")
    guards = Set("GuardDuty")


# Define the "GuardDuty" entity
class GuardDuty(db.Entity):
    _table_ = "GuardDuty"
    duty = Required(Duty, column="IdDuty")
    guard = Required(Guard, column="IdGuard")
    PrimaryKey(duty, guard)


# Define the "Prisoner" entity
class Prisoner(db.Entity):
    _table_ = "Prisoner"
    id_prisoner = PrimaryKey(int, column="IdPrisoner", auto=True)
    pesel = Required(str, column="PESEL")
    first_name = Required(str, column="FirstName")
    last_name = Required(str, column="LastName")
    admission_date = Required(datetime, column="AdmissionDate")
    id_cell = Required(Cell, column="IdCell")
    id_contact_person = Optional(ContactPerson, column="IdContactPerson")
    height = Optional(float, column="Height")
    blood_group = Optional(str, column="BloodGroup", nullable=True)
    sex = Required(str, column="Sex")
    id_prison = Required(Prison, column="IdPrison")
    sentences = Set("Sentence")
    visits = Set("Visit")
    examinations = Set("Examination")
    furloughs = Set("Furlough")


# Define the "Sentence" entity
class Sentence(db.Entity):
    _table_ = "Sentence"
    id_sentence = PrimaryKey(int, column="IdSentence", auto=True)
    article = Required(str, column="Article")
    paragraph = Required(int, column="Paragraph")
    stay_duration_days = Required(int, column="StayDurationDays")
    id_prisoner = Required(Prisoner, column="IdPrisoner")


# Define the "Visit" entity
class Visit(db.Entity):
    _table_ = "Visit"
    id_visit = PrimaryKey(int, column="IdVisit", auto=True)
    id_prisoner = Required(Prisoner, column="IdPrisoner")
    start_date = Required(datetime, column="StartDate")
    end_date = Required(datetime, column="EndDate")
    name = Required(str, column="Name")
    surname = Required(str, column="Surname")


# Define the "Examination" entity
class Examination(db.Entity):
    _table_ = "Examination"
    id_examination = PrimaryKey(int, column="IdExamination", auto=True)
    id_doctor = Required(Doctor, column="IdDoctor")
    id_prisoner = Required(Prisoner, column="IdPrisoner")
    examination_type = Required(str, column="ExaminationType")
    examination_date = Required(datetime, column="ExaminationDate")
    examination_result = Required(str, column="ExaminationResult")


# Define the "Furlough" entity
class Furlough(db.Entity):
    _table_ = "Furlough"
    id_furlough = PrimaryKey(int, column="IdFurlough", auto=True)
    id_prisoner = Required(Prisoner, column="IdPrisoner")
    start_date = Required(datetime, column="StartDate")
    end_date = Required(datetime, column="EndDate")
