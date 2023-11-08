CREATE INDEX idx_prisoner_names ON "Prisoner" ("FirstName", "LastName");
CREATE INDEX idx_prison_penitentiary ON  "Prison" ("PenitentiaryName");
CREATE INDEX idx_prisoner_pesel ON "Prisoner" ("PESEL");
CREATE INDEX idx_specialization ON "Specialization" ("Specialization");

CREATE INDEX idx_doctor_idspecialization ON "Doctor" ("IdSpecialization");

CREATE INDEX idx_examination_type ON "Examination"("ExaminationType");

CREATE INDEX idx_prisoner_ ON "Prisoner" ("IdPrison");
CREATE INDEX idx_guard_idprison ON public."Guard" ("IdPrison");

CREATE INDEX idx_duty_startdate ON public."Duty" ("StartDate");
CREATE INDEX idx_duty_enddate ON public."Duty" ("EndDate");


