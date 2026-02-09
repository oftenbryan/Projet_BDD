import datetime 
import mysql.connector
from connexion import connexionBDD,selectDB,fermerCnx

def requeteSimple(cnx, requete):
    try:
        with cnx.cursor() as cursor:
            cursor.execute(requete)
            return cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)


# Requete parametree (optimisation de l'execution multiple)
def requeteParametree(cnx):
    try:
        with cnx.cursor() as cursor:
            query = "SELECT idPokemon, horaire, duree\
					  FROM apparition\
					  WHERE horaire BETWEEN %s AND %s"
            debut = datetime.date(2016, 10, 1)
            fin = datetime.date(2016, 10, 30)
            cursor.execute(query, (debut, fin))
            for idPokemon, horaire, duree in cursor:
                print("{}, {}, {}".format(idPokemon, horaire, duree))
    except mysql.connector.Error as err:
        print(err)
    
def creer_bdd(cnx):
    s = ["DROP DATABASE IF EXISTS Population",
        "CREATE DATABASE Population",
        "USE Population",
        "DROP TABLE IF EXISTS Region",
        "DROP TABLE IF EXISTS Departement",
        "DROP TABLE IF EXISTS Ville",
        #"DROP TABLE IF EXISTS Recenser",
        "CREATE TABLE Region(\
           idRegion SMALLINT,\
           nomRegion VARCHAR(50),\
           PRIMARY KEY(idRegion)\
        )",
        "CREATE TABLE Departement(\
           idDepartement SMALLINT,\
           numeroDepartement VARCHAR(3),\
           nomDepartement VARCHAR(50),\
           idRegion SMALLINT NOT NULL,\
           PRIMARY KEY(idDepartement),\
           FOREIGN KEY(idRegion) REFERENCES Region(idRegion)\
        )",
        "CREATE TABLE Ville(\
           idVille INT,\
           codeGeo VARCHAR(5),\
           superficieVille DECIMAL(15,2),\
           nomVille VARCHAR(50),\
           idDepartement SMALLINT NOT NULL,\
           PRIMARY KEY(codeGeo),\
           FOREIGN KEY(idDepartement) REFERENCES Departement(idDepartement)\
        )"#,
#        "CREATE TABLE Recenser(\
#           idVille INT,\
#           annee SMALLINT,\
#           population INT,\
#           nbLogements DOUBLE,\
#           nbNaissances INT,\
#           nbDeces INT,\
#           PRIMARY KEY(idVille, annee),\
#           FOREIGN KEY(idVille) REFERENCES Ville(idVille)\
#        )"
    ]

    for requete in s:
        requeteSimple(cnx, requete)

