import datetime 
import mysql.connector
from connexion import connexionBDD,selectDB,fermerCnx
from import_data import regionSQL,departementSQL,villeEtArrSQL
from requetes import creer_bdd

cnx = connexionBDD()
creer_bdd(cnx)

regionSQL()
departementSQL()
villeEtArrSQL()

fermerCnx(cnx)