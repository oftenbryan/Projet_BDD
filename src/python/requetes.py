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

def testExecutionConnector():
    cnx = connexionBDD()
    selectDB(cnx, "Pokemons")
    rows = requeteSimple(cnx, "SELECT * FROM Pokemon")
    for rows in rows:
        print(rows)
    requeteParametree(cnx)
    fermerCnx(cnx)
    
# def creer_bdd():
    