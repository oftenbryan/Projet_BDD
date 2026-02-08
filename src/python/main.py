import datetime 
import mysql.connector
from connexion import connexionBDD,selectDB,fermerCnx
from requetes import creer_bdd

cnx = connexionBDD()
creer_bdd(cnx)

fermerCnx(cnx)