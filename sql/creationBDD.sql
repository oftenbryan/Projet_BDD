CREATE TABLE Region(
   idRegion SMALLINT,
   nomRegion VARCHAR(50),
   PRIMARY KEY(idRegion)
);

CREATE TABLE Departement(
   idDepartement SMALLINT,
   numeroDepartement VARCHAR(3),
   nomDepartement VARCHAR(50),
   idRegion SMALLINT NOT NULL,
   PRIMARY KEY(idDepartement),
   FOREIGN KEY(idRegion) REFERENCES Region(idRegion)
);

CREATE TABLE Ville(
   CODEGEO INT,
   superficieVille DECIMAL(15,2),
   nomVille VARCHAR(50),
   idDepartement SMALLINT NOT NULL,
   PRIMARY KEY(CODEGEO),
   FOREIGN KEY(idDepartement) REFERENCES Departement(idDepartement)
);

CREATE TABLE Recenser(
   CODEGEO INT,
   annee SMALLINT,
   population INT,
   nbLogements INT,
   nbNaissances INT,
   nbDeces INT,
   PRIMARY KEY(CODEGEO, annee),
   FOREIGN KEY(CODEGEO) REFERENCES Ville(CODEGEO)
);
