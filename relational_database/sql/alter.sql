CREATE TABLE "Stay" (
    "IdPrisoner" int4 NOT NULL,
    "IdCell" int4 NOT NULL,
    "StartDate" TIMESTAMP NOT NULL,
    "EndDate" TIMESTAMP NULL CHECK ("EndDate" >= "StartDate"),
	CONSTRAINT "FK_Prisoner.IdPrisoner" FOREIGN KEY ("IdPrisoner")
	    REFERENCES public."Prisoner"("IdPrisoner") ON DELETE CASCADE,
	CONSTRAINT "FK_Cell.IdCell" FOREIGN KEY ("IdCell") REFERENCES public."Cell"("IdCell")
);

INSERT INTO "Stay" (
    SELECT "IdPrisoner", "IdCell", NOW(), NULL FROM "Prisoner"
);

ALTER TABLE public."Prisoner" DROP COLUMN "IdCell"