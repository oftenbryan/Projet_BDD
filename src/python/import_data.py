import pandas as pd
from mysql.connector import errorcode
from sqlalchemy import create_engine

from connexion import login, mdp, machine # pyright: ignore

# Acces au fichier sql
sql_db_path = "../../sql/creationBDD.sql"

def importCSV(fichierCSV, carSepCsv):
    dataFrame = pd.read_csv(fichierCSV, sep=carSepCsv)
    return dataFrame

def dataFrameToMySQLTable(database, tableName, dataFrame):
    engine = create_engine(f"mysql+mysqlconnector://{login}:{mdp}@{machine}/{database}")
    # https://docs.sqlalchemy.org/en/20/core/engines.html
    # Creation de la table pokemonbis correspondant au fichier csv a partir du dataFrame
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    retour = dataFrame.to_sql(tableName, engine, if_exists="replace")
    print("\n", retour, tableName, " creees\n")
    # liberation de la connection SQLAlchemy
    engine.dispose()
    
def CSVToMySQLTable(fileNameCSV, database, tableName, carSepCsv=","):
    dataFrame = importCSV(fileNameCSV, carSepCsv)
    dataFrameToMySQLTable(database, tableName, dataFrame)
    
CSVToMySQLTable("../../data/raw/pokemonbis.csv", "Pokemons", "pokemonbis")