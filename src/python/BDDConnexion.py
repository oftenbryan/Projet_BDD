# -*- coding: utf-8 -*-
"""
@author: Renaud VERIN

Executer avant dans la Console Spyder et redemarrer la console apres :
conda install mysql-connector-python sqlalchemy pandas matplotlib

"""

import mysql.connector
from mysql.connector import errorcode
import datetime # utile juste pour l'exemple sur les dates
import pandas as pd
from sqlalchemy import create_engine

login='root'
with open("mdp.txt", "r") as f:
    mdp = f.read().strip()
# machine='127.0.0.1'
machine='localhost'

#####################################################################
# MySQL Connector
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

# Connexion sans acces a la base (sinon dernier parametre de connect)
# Retourne la connexion si pas d'erreur, None sinon
def connexionBDD():
	try:
		cnx = mysql.connector.connect(user=login, password=mdp,
	                               host='127.0.0.1')
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
		cnx = None
	return cnx

# Selection de la base
def selectDB(cnx, bdd):
	cnx.database=bdd

# Requete simple sans parametre
# Retourne une liste du resultat
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
			query = ('SELECT idPokemon, horaire, duree\
					  FROM apparition\
					  WHERE horaire BETWEEN %s AND %s')
			debut = datetime.date(2016, 10, 1)
			fin = datetime.date(2016, 10, 30)
			cursor.execute(query, (debut, fin))
			for (idPokemon, horaire, duree) in cursor:
				print("{}, {}, {}".format(idPokemon, horaire, duree))
	except mysql.connector.Error as err:
		print(err)

# Fermeture de la connexion
def fermerCnx(cnx):
	cnx.close()

# Test d'execution du connector
def testExecutionConnector():
	cnx = connexionBDD()
	selectDB(cnx, 'Pokemons')
	rows = requeteSimple(cnx, 'SELECT * FROM Pokemon')
	for rows in rows:
		print(rows)
	requeteParametree(cnx)
	fermerCnx(cnx)


#####################################################################
# Import d'un fichier csv par pandas
# pandas = librairie Python de gestion et analyse de données

# Lecture du csv de pokemonbis et conversion en un DataFrame pok par pandas
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
def importCSV(fichierCSV, carSepCsv):
	dataFrame=pd.read_csv(fichierCSV, sep=carSepCsv)
# 	print(dataFrame.columns)
# 	print(dataFrame)
	return dataFrame

#####################################################################
# Connexion SQLAlchemy a MySQL necessaire pour pandas
# SQLAlchemy = ORM (Object Relational Mapper)
def dataFrameToMySQLTable(database, tableName, dataFrame):
	# engine = create_engine("mysql+mysqlconnector://login:mdp@host/database")
	# https://docs.sqlalchemy.org/en/20/core/engines.html
	engine = create_engine('mysql+mysqlconnector://' + login +':' + mdp +'@' + machine + '/' + database)
	# Creation de la table pokemonbis correspondant au fichier csv a partir du dataFrame
	# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
	retour = dataFrame.to_sql(tableName, engine, if_exists='replace')
	print("\n", retour, tableName, " creees\n")
	# liberation de la connection SQLAlchemy
	engine.dispose()

def CSVToMySQLTable(fileNameCSV, database, tableName, carSepCsv=','):
	dataFrame=importCSV(fileNameCSV, carSepCsv)
	dataFrameToMySQLTable(database, tableName, dataFrame)


testExecutionConnector()
CSVToMySQLTable("/home/swaagoscar/Documents/M1/T2/programmation_base_de_donnee/Projet_BDD/data/raw/pokemonbis.csv", "Pokemons", "pokemonbis")