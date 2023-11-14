CREATE INDEX idx_prisoner_names ON "Prisoner" ("FirstName", "LastName");
CREATE INDEX idx_prison_name ON "Prison" ("PenitentiaryName");
CREATE INDEX idx_prisoner_pesel ON "Prisoner" ("PESEL");
CREATE INDEX idx_specialization ON "Specialization" ("Specialization");
CREATE INDEX idx_doctor_idspecialization ON "Doctor" ("IdSpecialization");
CREATE INDEX idx_examination_type ON "ExaminationType" ("ExaminationType");
CREATE INDEX idx_prisoner_idprison  ON "Prisoner" ("IdPrison");
CREATE INDEX idx_guard_idprison ON "Guard" ("IdPrison");
CREATE INDEX idx_duty_startdate ON "Duty" ("StartDate");
CREATE INDEX idx_duty_enddate ON "Duty" ("EndDate");
CREATE INDEX idx_guardduty_idduty ON "GuardDuty" ("IdDuty");
CREATE INDEX idx_examination_idprisoner ON "Examination" ("IdPrisoner");
CREATE INDEX idx_guard_idrank ON public."Guard" ("IdRank");

