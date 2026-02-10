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
    # Affiche les resultats d'une requete
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

    # on effectue les requetes une par une
    for req in requetes:
        requeteSimple(cnx, req)


def usePopulation(cnx):
    requeteSimple(cnx, "USE Population")


def vues(cnx):
    # supprime les vues si elles existent deja
    requeteSimple(cnx, "DROP VIEW IF EXISTS villeSeule")
    requeteSimple(cnx, "DROP VIEW IF EXISTS arrondissement")

    # cree les vues pour separer villes et arrondissements
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


def requete_f_naissance_villes():
    """f) Liste des 10 villes ou on nait le plus."""
    return """
    SELECT 
        vs.nomVille, d.nomDepartement,
        SUM(rcs.nbNaissances) as totalNaissances
    FROM Recenser rcs 
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    GROUP BY vs.idVille, vs.nomVille, d.nomDepartement
    ORDER BY totalNaissances DESC LIMIT 10
    """


def requete_f_deces_villes():
    """f) Liste des 10 villes ou on meurt le plus."""
    return """
    SELECT 
        vs.nomVille, d.nomDepartement,
        SUM(rcs.nbDeces) as totalDeces
    FROM Recenser rcs 
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    GROUP BY vs.idVille, vs.nomVille, d.nomDepartement
    ORDER BY totalDeces DESC LIMIT 10
    """


def requete_f_naissance_departements():
    """f) Liste des 10 departements ou on nait le plus."""
    return """
    SELECT 
        d.nomDepartement,
        SUM(rcs.nbNaissances) as totalNaissances
    FROM Recenser rcs 
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    GROUP BY d.idDepartement, d.nomDepartement
    ORDER BY totalNaissances DESC LIMIT 10
    """


def requete_f_deces_departements():
    """f) Liste des 10 departements ou on meurt le plus."""
    return """
    SELECT 
        d.nomDepartement,
        SUM(rcs.nbDeces) as totalDeces
    FROM Recenser rcs 
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    GROUP BY d.idDepartement, d.nomDepartement
    ORDER BY totalDeces DESC LIMIT 10
    """


def requete_g_villes_grande():
    """g) Liste des 10 villes avec la plus grande densite."""
    return """
    SELECT
        vs.nomVille,
        d.nomDepartement,
        AVG(rcs.population) / vs.superficieVille AS densitePop
    FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    WHERE vs.superficieVille > 0
    GROUP BY vs.idVille, vs.nomVille, d.nomDepartement, vs.superficieVille
    ORDER BY densitePop DESC
    LIMIT 10
    """


def requete_g_villes_petite():
    """g) Liste des 10 villes avec la plus petite densite."""
    return """
    SELECT
        vs.nomVille,
        d.nomDepartement,
        AVG(rcs.population) / vs.superficieVille AS densitePop
    FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    WHERE vs.superficieVille > 0
    GROUP BY vs.idVille, vs.nomVille, d.nomDepartement, vs.superficieVille
    ORDER BY densitePop ASC
    LIMIT 10
    """


def requete_g_departements_grande():
    """g) Liste des 10 departements avec la plus grande densite."""
    return """
    SELECT
        d.nomDepartement,
        SUM(rcs.population) / SUM(vs.superficieVille) AS densitePop
    FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    WHERE vs.superficieVille > 0
    GROUP BY d.idDepartement, d.nomDepartement
    ORDER BY densitePop DESC
    LIMIT 10
    """


def requete_g_departements_petite():
    """g) Liste des 10 departements avec la plus petite densite."""
    return """
    SELECT
        d.nomDepartement,
        SUM(rcs.population) / SUM(vs.superficieVille) AS densitePop
    FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
    WHERE vs.superficieVille > 0
    GROUP BY d.idDepartement, d.nomDepartement
    ORDER BY densitePop ASC
    LIMIT 10
    """


def requete_h_departement():
    """h) Comparaison pour 2020 des naissances / deces / mouvements de population par departement."""
    return """
    WITH stats1968Dpt AS (
        SELECT d.idDepartement, d.nomDepartement,
               SUM(rcs.population) AS pop1968,
               SUM(rcs.nbNaissances) AS nais1968,
               SUM(rcs.nbDeces) AS deces1968
        FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
        WHERE rcs.annee = 1968
        GROUP BY d.idDepartement, d.nomDepartement
    ),
    stats2020Dpt AS (
        SELECT d.idDepartement, d.nomDepartement,
               SUM(rcs.population) AS pop2020,
               SUM(rcs.nbNaissances) AS nais2020,
               SUM(rcs.nbDeces) AS deces2020
        FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
        WHERE rcs.annee = 2020
        GROUP BY d.idDepartement, d.nomDepartement
    )
    SELECT
        s20.nomDepartement,
        s20.nais2020 AS naissances,
        s20.deces2020 AS deces,
        (s20.pop2020 - s68.pop1968) AS deltaPop,
        (s20.pop2020 - s68.pop1968) - (s20.nais2020 - s20.deces2020) AS mouvements
    FROM stats2020Dpt s20
    JOIN stats1968Dpt s68 ON s20.idDepartement = s68.idDepartement
    """


def requete_h_region():
    """h) Comparaison pour 2020 des naissances / deces / mouvements de population par region."""
    return """
    WITH stats1968Reg AS (
        SELECT reg.idRegion, reg.nomRegion,
               SUM(rcs.population) AS pop1968,
               SUM(rcs.nbNaissances) AS nais1968,
               SUM(rcs.nbDeces) AS deces1968
        FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
        JOIN Region reg ON d.idRegion = reg.idRegion
        WHERE rcs.annee = 1968
        GROUP BY reg.idRegion, reg.nomRegion
    ),
    stats2020Reg AS (
        SELECT reg.idRegion, reg.nomRegion,
               SUM(rcs.population) AS pop2020,
               SUM(rcs.nbNaissances) AS nais2020,
               SUM(rcs.nbDeces) AS deces2020
        FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        JOIN Departement d ON vs.idDepartement = d.idDepartement
        JOIN Region reg ON d.idRegion = reg.idRegion
        WHERE rcs.annee = 2020
        GROUP BY reg.idRegion, reg.nomRegion
    )
    SELECT
        s20.nomRegion,
        s20.nais2020 AS naissances,
        s20.deces2020 AS deces,
        (s20.pop2020 - s68.pop1968) AS deltaPop,
        (s20.pop2020 - s68.pop1968) - (s20.nais2020 - s20.deces2020) AS mouvements
    FROM stats2020Reg s20
    JOIN stats1968Reg s68 ON s20.idRegion = s68.idRegion
    """


def requete_i():
    """i) Comparaison par recensement des naissances / deces / mouvements de population de la France."""
    return """
    WITH stats AS (
        SELECT 
            rcs.annee,
            SUM(rcs.population) AS population,
            SUM(rcs.nbNaissances) AS naissances,
            SUM(rcs.nbDeces) AS deces
        FROM Recenser rcs
        JOIN villeSeule vs ON rcs.idVille = vs.idVille
        GROUP BY rcs.annee
    )
    SELECT 
        annee,
        naissances,
        deces,
        population - LAG(population) OVER (ORDER BY annee) AS deltaPop,
        (population - LAG(population) OVER (ORDER BY annee)) - (naissances - deces) AS mouvements
    FROM stats
    ORDER BY annee
    """


def requete_1():
    """Donner le nombre de villes en Normandie"""
    return """
    SELECT COUNT(*) AS nbVille
    FROM villeSeule vs
        JOIN Departement d ON vs.idDepartement = d.idDepartement
        JOIN Region reg ON d.idRegion = reg.idRegion
    WHERE LOWER(reg.nomRegion) = "normandie"
    """


def requete_2():
    """Donner les villes de la Creuse qui sont plus peuplées que la moyenne des communes françaises en 2020"""
    return """
    SELECT vs.nomVille, rcs.population
    FROM villeSeule vs
        JOIN Departement d ON vs.idDepartement = d.idDepartement
        JOIN Recenser rcs ON rcs.idVille = vs.idVille AND rcs.annee = 2020
    WHERE LOWER(d.nomDepartement) = "creuse"
        AND rcs.population > (
            SELECT AVG(rcs.population)
            FROM Recenser rcs
            WHERE rcs.annee = 2020
            )
    ORDER BY rcs.population DESC
    """


def requete_3():
    """Ville morte etc"""
    return """
    WITH deces AS (
		    SELECT vs.idVille, vs.nomVille, rcs.nbDeces
		    FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille AND rcs.annee = 2020
	    ),
        pop2014 AS (
		    SELECT vs.idVille, vs.nomVille, rcs.population population
            FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille AND rcs.annee = 2014
	    )

    SELECT (d.nbDeces / p14.population) ratioDeces, d.nomVille
    FROM deces d JOIN pop2014 p14 ON d.idVille = p14.idVille
    ORDER BY ratioDeces DESC LIMIT 10
    """


def requete_4():
    return 0


def requete_5():
    return 0
