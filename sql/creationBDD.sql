DROP DATABASE IF EXISTS Recensement;
CREATE DATABASE Recensement;
USE Recensement;

-- Region = (idRegion SMALLINT, nomRegion VARCHAR(50));
-- Departement = (idDepartement SMALLINT, numeroDepartement VARCHAR(3), nomDepartement VARCHAR(50), #idRegion);
-- Ville = (codeGeo INT, superficieVille DECIMAL(15,2), nomVille VARCHAR(50), #idDepartement);
-- Recenser = (#codeGeo, annee SMALLINT, population INT, nbLogements INT, nbNaissances INT, nbDeces INT);

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
   codeGeo INT,
   superficieVille DECIMAL(15,2),
   nomVille VARCHAR(50),
   idDepartement SMALLINT NOT NULL,
   PRIMARY KEY(codeGeo),
   FOREIGN KEY(idDepartement) REFERENCES Departement(idDepartement)
);

CREATE TABLE Recenser(
   codeGeo INT,
   annee SMALLINT,
   population INT,
   nbLogements INT,
   nbNaissances INT,
   nbDeces INT,
   PRIMARY KEY(codeGeo, annee),
   FOREIGN KEY(codeGeo) REFERENCES Ville(codeGeo)
);
