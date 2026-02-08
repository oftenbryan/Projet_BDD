import pandas as pd
from mysql.connector import errorcode
from sqlalchemy import create_engine

from connexion import login, mdp, machine # pyright: ignore

# Acces au fichier sql
#sql_db_path = "../../sql/creationBDD.sql"

#def importCSV(fichierCSV, carSepCsv):
#    dataFrame = pd.read_csv(fichierCSV, sep=carSepCsv)
#    return dataFrame

def dataFrameToMySQLTable(database, tableName, dataFrame):
    engine = create_engine(f"mysql+mysqlconnector://{login}:{mdp}@{machine}/{database}")
    # https://docs.sqlalchemy.org/en/20/core/engines.html
    # Creation de la table pokemonbis correspondant au fichier csv a partir du dataFrame
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    retour = dataFrame.to_sql(tableName, engine, if_exists="replace")
    print("\n", retour, tableName, " creees\n")
    # liberation de la connection SQLAlchemy
    engine.dispose()
    
#def CSVToMySQLTable(fileNameCSV, database, tableName, carSepCsv=","):
#    dataFrame = importCSV(fileNameCSV, carSepCsv)
#    dataFrameToMySQLTable(database, tableName, dataFrame)



def regionSQL():
    popDep = pd.read_csv("../../data/raw/populationDepartementsFrance.csv", sep=",")
    dfRegion = pd.DataFrame({'idRegion' : popDep['codeRegion'], 'nomRegion' : popDep['nomRegion']}).drop_duplicates(subset = ["idRegion"]).set_index("idRegion")
    dataFrameToMySQLTable("Population", "Region", dfRegion)


def departementSQL():
    popDep = pd.read_csv("../../data/raw/populationDepartementsFrance.csv", sep=",")
    dfDepartement = pd.DataFrame({'numeroDepartement' : popDep['codeDepart'], 'nomDepartement' : popDep['nomDepart'], 'idRegion' : popDep['codeRegion']})
    dfDepartement.index.names = ["idDepartement"]
    dataFrameToMySQLTable("Population", "Departement", dfDepartement)

def codeToDep(df):
    df = str(df)
    if (len(df) == 4):
        return df[:1]
    elif df[:2] in ['97']:
        return df[:3]
    else:
        return df[:2]

def villeSQL():
    popMeta = pd.read_csv("../../data/raw/populationMetaDataSerieHistorique2020.csv", sep=";")
    popSerie = pd.read_csv("../../data/raw/populationSerieHistorique2020.csv", sep=";")

    dfMetaVille = pd.DataFrame({'idVille' : popMeta['COD_MOD'], 'nomVille' : popMeta['LIB_MOD']}).dropna().reset_index()

    dfTmp = pd.DataFrame({'codeGeo' : popSerie['CODGEO']})

    dfTmp['codeGeo'] = dfTmp['codeGeo'].apply(codeToDep)

    dfVille = pd.DataFrame({'codeGeo' : popSerie['CODGEO'], 'superficieVille' : popSerie['SUPERF'], 'nomVille' : dfMetaVille['nomVille'], 'idDepartement' : dfTmp['codeGeo']})
    dfVille.index.names = ["idVille"]

    dataFrameToMySQLTable("Population", "Ville", dfVille)


regionSQL()
departementSQL()
#villeSQL()
