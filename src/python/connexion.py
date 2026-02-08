"""
Script pour se connecter à la database
"""

import mysql.connector
from mysql.connector import errorcode

# Identifiants
login = "root"
with open("mdp.txt", "r") as f:
    mdp = f.read().strip()
host = "127.0.0.1"
machine = "localhost"


# Connextion à MySQL
def connexionBDD():
    try:
        cnx = mysql.connector.connect(user=login, password=mdp, host=host)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        cnx = None
    return cnx
    
# Selection de la base de données
def selectDB(cnx, bdd):
    cnx.database = bdd

# Terminer notre connexion à MySQL
def fermerCnx(cnx):
    cnx.close()
