DROP DATABASE IF EXISTS Population;
CREATE DATABASE Population;
USE Population;

-- Region = (idRegion SMALLINT, nomRegion VARCHAR(50));
-- Departement = (idDepartement SMALLINT, numeroDepartement VARCHAR(3), nomDepartement VARCHAR(50), #idRegion);
-- Ville = (idVille INT, superficieVille DECIMAL(15,2), nomVille VARCHAR(50), #idDepartement);
-- Recenser = (#idVille, annee SMALLINT, population INT, nbLogements INT, nbNaissances INT, nbDeces INT);

DROP TABLE IF EXISTS Region;
DROP TABLE IF EXISTS Departement;
DROP TABLE IF EXISTS Ville;
DROP TABLE IF EXISTS Recenser;

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
   idVille INT,
   codeGeo VARCHAR(5),
   superficieVille DECIMAL(15,2),
   nomVille VARCHAR(50),
   idDepartement SMALLINT NOT NULL,
   PRIMARY KEY(idVille),
   FOREIGN KEY(idDepartement) REFERENCES Departement(idDepartement)
);

CREATE TABLE Recenser(
   idVille INT,
   annee SMALLINT,
   population INT,
   nbLogements DOUBLE,
   nbNaissances INT,
   nbDeces INT,
   PRIMARY KEY(idVille, annee),
   FOREIGN KEY(idVille) REFERENCES Ville(idVille)
);