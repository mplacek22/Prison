-- public."CellType" definition

CREATE TABLE public."CellType" (
	"IdCellType" int4 NOT NULL,
	"CellType" varchar(15) NOT NULL,
	CONSTRAINT "CellType_pkey" PRIMARY KEY ("IdCellType")
);


-- public."ContactPerson" definition

CREATE TABLE public."ContactPerson" (
	"IdContactPerson" int4 NOT NULL,
	"Name" varchar(30) NOT NULL,
	"Surname" varchar(30) NOT NULL,
	"Kinship" varchar(30) NULL,
	"PhoneNr" varchar(30) NULL,
	CONSTRAINT "ContactPerson_pkey" PRIMARY KEY ("IdContactPerson")
);


-- public."Doctor" definition


CREATE TABLE public."Doctor" (
	"IdDoctor" int4 NOT NULL,
	"PESEL" varchar(11) NOT NULL,
	"Name" varchar(30) NOT NULL,
	"Surname" varchar(30) NOT NULL,
	"Specialization" varchar(30) NOT NULL,
	CONSTRAINT "Doctor_pkey" PRIMARY KEY ("IdDoctor")
);


-- public."Prison" definition

CREATE TABLE public."Prison" (
	"idPrison" int4 NOT NULL,
	"PenitentiaryName" varchar(30) NOT NULL,
	"City" varchar(30) NOT NULL,
	"Street" varchar(60) NOT NULL,
	"BuildingNr" varchar(5) NOT NULL,
	"ApartmentNr" varchar(5) NULL,
	CONSTRAINT "Prison_pkey" PRIMARY KEY ("idPrison")
);


-- public."AdministrativeEmployee" definition

CREATE TABLE public."AdministrativeEmployee" (
	"IdEmployee" int4 NOT NULL,
	"PESEL" varchar(11) NOT NULL CHECK (LENGTH("PESEL") = 11),
	"Name" varchar(30) NOT NULL,
	"Surname" varchar(30) NOT NULL,
	"idPrison" int4 NOT NULL,
	CONSTRAINT "AdministrativeEmployee_pkey" PRIMARY KEY ("IdEmployee"),
	CONSTRAINT "FK_AdministrativeEmployee.idPrison" FOREIGN KEY ("idPrison") REFERENCES public."Prison"("idPrison")
);


-- public."Building" definition

CREATE TABLE public."Building" (
	"IdBuilding" int4 NOT NULL,
	"City" varchar(30) NOT NULL,
	"Street" varchar(60) NOT NULL,
	"BuildingNr" varchar(5) NOT NULL,
	"idPrison" int4 NOT NULL,
	CONSTRAINT "Building_pkey" PRIMARY KEY ("IdBuilding"),
	CONSTRAINT "FK_Building.idPrison" FOREIGN KEY ("idPrison") REFERENCES public."Prison"("idPrison")
);


-- public."Guard" definition

CREATE TABLE public."Guard" (
	"IdGuard" int4 NOT NULL,
	"PESEL" varchar(11) NOT NULL CHECK(Length("PESEL") = 11),
	"Name" varchar(30) NOT NULL,
	"Surname" varchar(30) NOT NULL,
	"Rank" varchar(30) NULL,
	"idPrison" int4 NOT NULL,
	CONSTRAINT "Guard_pkey" PRIMARY KEY ("IdGuard"),
	CONSTRAINT "FK_Guard.idPrison" FOREIGN KEY ("idPrison") REFERENCES public."Prison"("idPrison")
);


-- public."User" definition

CREATE TABLE public."User" (
	"Username" varchar(30) NOT NULL,
	"Password" varchar(30) NOT NULL,
	"IdEmployee" int4 NULL,
	"IdGuard" int4 NULL,
	"IdDoctor" int4 NULL,
	CONSTRAINT "User_pkey" PRIMARY KEY ("Username"),
	CONSTRAINT "FK_USER.IdDoctor" FOREIGN KEY ("IdDoctor") REFERENCES public."Doctor"("IdDoctor"),
	CONSTRAINT "FK_USER.IdGuard" FOREIGN KEY ("IdGuard") REFERENCES public."Guard"("IdGuard"),
	CONSTRAINT "FK_User.IdEmployee" FOREIGN KEY ("IdEmployee") REFERENCES public."AdministrativeEmployee"("IdEmployee"),
	CONSTRAINT "User_type" CHECK (("IdDoctor" IS NOT NULL)::integer + ("IdGuard" IS NOT NULL)::integer + ("IdEmployee" IS NOT NULL)::integer = 1)

);


-- public."Block" definition

CREATE TABLE public."Block" (
	"IdBlok" int4 NOT NULL,
	"BlockName" varchar(30) NOT NULL,
	"IdBuilding" int4 NOT NULL,
	CONSTRAINT "Block_pkey" PRIMARY KEY ("IdBlok"),
	CONSTRAINT "FK_Block.IdBuilding" FOREIGN KEY ("IdBuilding") REFERENCES public."Building"("IdBuilding")
);


-- public."Cell" definition

CREATE TABLE public."Cell" (
	"IdCell" int4 NOT NULL,
	"CellNr" int4 NOT NULL,
	"IdCellType" int4 NOT NULL,
	"CellCapacity" int2 NOT NULL CHECK ("CellCapacity" > 0),
	"IdBlock" int4 NOT NULL,
	CONSTRAINT "Cell_pkey" PRIMARY KEY ("IdCell"),
	CONSTRAINT "FK_Cell.IdBlock" FOREIGN KEY ("IdBlock") REFERENCES public."Block"("IdBlok"),
	CONSTRAINT "FK_Cell.IdCellType" FOREIGN KEY ("IdCellType") REFERENCES public."CellType"("IdCellType")
);


-- public."Duty" definition

CREATE TABLE public."Duty" (
	"IdDuty" int4 NOT NULL,
	"StartDate" timestamp NOT NULL,
	"EndDate" timestamp NOT NULL CHECK ("EndDate" > "StartDate"),
	"IdBlock" int4 NOT NULL,
	CONSTRAINT "Duty_pkey" PRIMARY KEY ("IdDuty"),
	CONSTRAINT "FK_Duty.IdBlock" FOREIGN KEY ("IdBlock") REFERENCES public."Block"("IdBlok")
);


-- public."GuardDuty" definition

CREATE TABLE public."GuardDuty" (
	"IdDuty" int4 NOT NULL,
	"IdGuard" int4 NOT NULL,
	CONSTRAINT "FK_GuardDuty.IdDuty" FOREIGN KEY ("IdDuty") REFERENCES public."Duty"("IdDuty"),
	CONSTRAINT "FK_GuardDuty.IdGuard" FOREIGN KEY ("IdGuard") REFERENCES public."Guard"("IdGuard")
);


CREATE TYPE blood_group AS ENUM ('A+', 'A-', 'B+', 'B-', 'AB+','AB-', '0+','0-', '');
CREATE TYPE sex AS ENUM ('F', 'M');

-- public."Prisoner" definition

CREATE TABLE public."Prisoner" (
	"IdPrisoner" int4 NOT NULL,
	"PESEL" varchar(11) NOT NULL CHECK (LENGTH("PESEL") = 11),
	"FirstName" varchar(30) NOT NULL,
	"LastName" varchar(30) NOT NULL,
	"AdmissionDate" timestamp NOT NULL,
	"IdCell" int4 NOT NULL,
	"IdContactPerson" int4 NULL,
	"Height" float4 NULL CHECK ("Height" > 0),
	"BloodGroup" blood_group NULL,
	"Sex" sex NOT NULL,
	CONSTRAINT "Prisoner_pkey" PRIMARY KEY ("IdPrisoner"),
	CONSTRAINT "FK_Prisoner.IdCell" FOREIGN KEY ("IdCell") REFERENCES public."Cell"("IdCell"),
	CONSTRAINT "FK_Prisoner.IdContactPerson" FOREIGN KEY ("IdContactPerson") REFERENCES public."ContactPerson"("IdContactPerson")
);


-- public."Sentence" definition

CREATE TABLE public."Sentence" (
	"IdSentence" int4 NOT NULL,
	"Article" varchar(10) NOT NULL,
	"Paragraph" int2 NOT NULL,
	"StayDurationDays" int2 NOT NULL CHECK ("StayDurationDays" > 0),
	"IdPrisoner" int4 NOT NULL,
	CONSTRAINT "Sentence_pkey" PRIMARY KEY ("IdSentence"),
	CONSTRAINT "FK_Sentence.IdPrisoner" FOREIGN KEY ("IdPrisoner") REFERENCES public."Prisoner"("IdPrisoner")
);


-- public."Visit" definition

CREATE TABLE public."Visit" (
	"IdVisit" int4 NOT NULL,
	"IdPrisoner" int4 NOT NULL,
	"StartDate" timestamp NOT NULL,
	"EndDate" timestamp NOT NULL CHECK("EndDate" > "StartDate"),
	"Name" varchar(30) NOT NULL,
	"Surname" varchar(30) NOT NULL,
	CONSTRAINT "Visit_pkey" PRIMARY KEY ("IdVisit"),
	CONSTRAINT "FK_Visit.IdPrisoner" FOREIGN KEY ("IdPrisoner") REFERENCES public."Prisoner"("IdPrisoner")
);


-- public."Examination" definition

CREATE TABLE public."Examination" (
	"IdExamination" int4 NOT NULL,
	"IdDoctor" int4 NOT NULL,
	"IdPrisoner" int4 NOT NULL,
	"ExaminationType" varchar(50) NOT NULL,
	"ExaminationDate" timestamp NOT NULL,
	"ExaminationResult" varchar(500) NOT NULL,
	CONSTRAINT "Examination_pkey" PRIMARY KEY ("IdExamination"),
	CONSTRAINT "FK_Examination.IdDoctor" FOREIGN KEY ("IdDoctor") REFERENCES public."Doctor"("IdDoctor"),
	CONSTRAINT "FK_Examination.IdPrisoner" FOREIGN KEY ("IdPrisoner") REFERENCES public."Prisoner"("IdPrisoner")
);


-- public."Furlough" definition

CREATE TABLE public."Furlough" (
	"IdFurlough" int4 NOT NULL,
	"IdPrisoner" int4 NOT NULL,
	"StartDate" timestamp NOT NULL,
	"EndDate" timestamp NOT NULL CHECK ("EndDate" > "StartDate"),
	CONSTRAINT "Furlough_pkey" PRIMARY KEY ("IdFurlough"),
	CONSTRAINT "FK_Furlough.IdPrisoner" FOREIGN KEY ("IdPrisoner") REFERENCES public."Prisoner"("IdPrisoner")
);
