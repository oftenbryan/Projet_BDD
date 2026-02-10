import datetime
import mysql.connector
from connexion import connexionBDD, selectDB, fermerCnx


def requeteSimple(cnx, requete):
    try:
        with cnx.cursor() as cursor:
            cursor.execute(requete)
            return cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)


def afficher_resultat(resultat, n=None):
    """Affiche les resultats d'une requete"""
    if resultat:
        if n:
            for row in resultat[:n]:
                print(row)
        else:
            for row in resultat:
                print(row)


def creer_bdd(cnx):
    requetes = [
        "DROP DATABASE IF EXISTS Population",
        "CREATE DATABASE Population",
        "USE Population",
        "DROP TABLE IF EXISTS Region",
        "DROP TABLE IF EXISTS Departement",
        "DROP TABLE IF EXISTS Ville",
        "DROP TABLE IF EXISTS Recenser",
        """
        CREATE TABLE Region(
           idRegion SMALLINT,
           nomRegion VARCHAR(50),
           PRIMARY KEY(idRegion)
        )
        """,
        """
        CREATE TABLE Departement(
           idDepartement SMALLINT,
           numeroDepartement VARCHAR(3),
           nomDepartement VARCHAR(50),
           idRegion SMALLINT NOT NULL,
           PRIMARY KEY(idDepartement),
           FOREIGN KEY(idRegion) REFERENCES Region(idRegion)
        )
        """,
        """
        CREATE TABLE Ville(
           idVille INT,
           codeGeo VARCHAR(5),
           superficieVille DECIMAL(15,2),
           nomVille VARCHAR(50),
           idDepartement SMALLINT NOT NULL,
           PRIMARY KEY(idVille),
           FOREIGN KEY(idDepartement) REFERENCES Departement(idDepartement)
        )
        """,
        """
        CREATE TABLE Recenser(
           idVille INT,
           annee SMALLINT,
           population INT,
           nbLogement DOUBLE,
           nbNaissances INT,
           nbDeces INT,
           PRIMARY KEY(idVille, annee),
           FOREIGN KEY(idVille) REFERENCES Ville(idVille)
        )
        """,
    ]
    for req in requetes:
        requeteSimple(cnx, req)


def usePopulation(cnx):
    requeteSimple(cnx, "USE Population")


def vues(cnx):
    # Supprime les vues si elles existent deja
    requeteSimple(cnx, "DROP VIEW IF EXISTS villeSeule")
    requeteSimple(cnx, "DROP VIEW IF EXISTS arrondissement")

    # Cree les vues pour separer villes et arrondissements
    requetes = [
        """
        CREATE VIEW villeSeule AS (
            SELECT *
            FROM Ville
            WHERE LOWER(nomVille) NOT LIKE '%arrondissement'
        )
        """,
        """
        CREATE VIEW arrondissement AS (
            SELECT *
            FROM Ville
            WHERE LOWER(nomVille) LIKE '%arrondissement'
        )
        """,
    ]
    for req in requetes:
        requeteSimple(cnx, req)


# ============================================================================
# REQUETES DU PROJET - QUESTIONS a a i
# ============================================================================


def requete_a():
    """a) Liste des populations en 2020 avec le nom de ville, departement, region."""
    return """
    SELECT rcs.population, vs.nomVille, d.nomDepartement, reg.nomRegion
    FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
                      JOIN Departement d ON vs.idDepartement = d.idDepartement
                      JOIN Region reg ON d.idRegion = reg.idRegion
    WHERE rcs.annee = 2020
    ORDER BY population DESC
    """


def requete_b():
    """b) Evolution de la population francaise de 1968 a 2020."""
    return """
    SELECT rcs.annee, SUM(rcs.population) AS populationFrance
    FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
    GROUP BY rcs.annee
    ORDER BY rcs.annee
    """


def requete_c_departement():
    """c) Liste des populations en 2020 par departement."""
    return """
    SELECT d.idDepartement AS idDep, d.nomDepartement AS nomDep, SUM(rcs.population) AS populationDep
    FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
                      JOIN Departement d ON vs.idDepartement = d.idDepartement
    WHERE rcs.annee = 2020
    GROUP BY idDep, nomDep
    ORDER BY populationDep DESC
    """


def requete_c_region():
    """c) Liste des populations en 2020 par region."""
    return """
    SELECT reg.idRegion AS idReg, reg.nomRegion AS nomReg, SUM(rcs.population) AS populationReg
    FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
                      JOIN Departement d ON vs.idDepartement = d.idDepartement
                      JOIN Region reg ON d.idRegion = reg.idRegion
    WHERE rcs.annee = 2020
    GROUP BY idReg, nomReg
    ORDER BY populationReg DESC
    """


def requete_d_paris_ville():
    """d) Population de Paris (ville)."""
    return """
    SELECT SUM(rcs.population) AS populationParis
    FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
    WHERE annee = 2020 AND LOWER(vs.nomVille) LIKE 'paris'
    """

def requete_d_paris_arr():
    """d) Population de Paris (arrondissements)."""
    return """
    SELECT SUM(rcs.population) AS populationParisArr
    FROM Recenser rcs JOIN arrondissement a ON rcs.idVille = a.idVille
    WHERE annee = 2020 AND LOWER(a.nomVille) LIKE 'paris%'
    """



def requete_e_villes():
    """e) Top 10 des villes ayant le plus grandi de 1968 a 2020."""
    return """
    WITH population2020 AS (
        SELECT vs.idVille, vs.nomVille, rcs.population AS popVille
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
        WHERE rcs.annee = 2020
    ),
    population1968 AS (
        SELECT vs.idVille, vs.nomVille, rcs.population AS popVille
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
        WHERE rcs.annee = 1968
    )
    SELECT pop20.nomVille, (pop20.popVille - pop68.popVille) AS croissanceVille
    FROM population2020 pop20 JOIN population1968 pop68 ON pop20.idVille = pop68.idVille
    ORDER BY croissanceVille DESC LIMIT 10
    """


def requete_e_departements():
    """e) Top 10 des departements ayant le plus grandi de 1968 a 2020."""
    return """
    WITH popDep2020 AS (
        SELECT d.idDepartement AS idDep, d.nomDepartement AS nomDep, SUM(rcs.population) AS popDep
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
                          JOIN Departement d ON vs.idDepartement = d.idDepartement
        WHERE rcs.annee = 2020
        GROUP BY idDep, nomDep
    ),
    popDep1968 AS (
        SELECT d.idDepartement AS idDep, d.nomDepartement AS nomDep, SUM(rcs.population) AS popDep
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
                          JOIN Departement d ON vs.idDepartement = d.idDepartement
        WHERE rcs.annee = 1968
        GROUP BY idDep, nomDep
    )
    SELECT d20.nomDep, (d20.popDep - d68.popDep) AS croissanceDep
    FROM popDep2020 d20 JOIN popDep1968 d68 ON d20.idDep = d68.idDep
    ORDER BY croissanceDep DESC LIMIT 10
    """


def requete_e_region():
    """e) Top des regions par croissance (1968-2020) - TODO: probleme de resultat."""
    return """
    WITH popReg2020 AS (
        SELECT reg.idRegion, reg.nomRegion, SUM(rcs.population) AS popRegion
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
                          JOIN Departement d ON vs.idDepartement = d.idDepartement
                          JOIN Region reg ON d.idRegion = reg.idRegion
        WHERE rcs.annee = 2020
        GROUP BY idRegion, nomRegion
    ),
    popReg1968 AS (
        SELECT reg.idRegion, reg.nomRegion, SUM(rcs.population) AS popRegion
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
                          JOIN Departement d ON vs.idDepartement = d.idDepartement
                          JOIN Region reg ON d.idRegion = reg.idRegion
        WHERE rcs.annee = 1968
        GROUP BY idRegion, nomRegion
    ),
    croissanceReg AS (
        SELECT r20.nomRegion, (r20.popRegion - r68.popRegion) AS croissanceRegion
        FROM popReg2020 r20 JOIN popReg1968 r68 ON r20.idRegion = r68.idRegion
        ORDER BY croissanceRegion DESC)
    SELECT SUM(cr.croissanceRegion) AS croissanceFr FROM croissanceReg cr
    """


def requete_f_naissance(cnx):
    """f) Liste des 10 villes / departements ou on nait le plus."""
    
    requeteN = """
    SELECT 
	vs.nomVille, 
        SUM(rcs.nbNaissances) as totalNaissances
    FROM recenser rcs 
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
    GROUP BY vs.idVille, vs.nomVille
    ORDER BY totalNaissances DESC LIMIT 10
    """
    resultat = requeteSimple(cnx,requeteN)
    if resultat:
        for row in resultat:
            print(row)
            
def requete_f_deces(cnx):
    """f) Liste des 10 villes / departements ou on meurt le plus."""
    
    requeteD = """
    SELECT 
	vs.nomVille, 
        SUM(rcs.nbDeces) as totalDeces
    FROM recenser rcs 
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
    GROUP BY vs.idVille, vs.nomVille
    ORDER BY totalDeces DESC LIMIT 10
    """
    resultat = requeteSimple(cnx,requeteD)
    if resultat:
        for row in resultat:
            print(row)


# ============================================================================
# REQUETES A FAIRE (TODO)
# ============================================================================

def requete_g(cnx):
    """g) Liste des 10 villes / departements avec la plus grande/petite densite."""
    # TODO: A implementer
    print("TODO: requete_g a implementer")
    pass


def requete_h(cnx):
    """h) Comparaison pour 2020 des naissances / deces / mouvements de population."""
    # TODO: A implementer
    print("TODO: requete_h a implementer")
    pass


def requete_i(cnx):
    """i) Comparaison par recensement des naissances / deces / mouvements de population de la France."""
    # TODO: A implementer
    print("TODO: requete_i a implementer")
    pass
