import pandas as pd
from mysql.connector import errorcode
from sqlalchemy import create_engine
from connexion import login, mdp, machine


def dataFrameToMySQLTable(database, tableName, dataFrame):
    engine = create_engine(f"mysql+mysqlconnector://{login}:{mdp}@{machine}/{database}")
    # https://docs.sqlalchemy.org/en/20/core/engines.html
    # Creation de la table pokemonbis correspondant au fichier csv a partir du dataFrame
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    retour = dataFrame.to_sql(tableName, engine, if_exists="append")
    print("\n", retour, tableName, " creees\n")
    # liberation de la connection SQLAlchemy
    engine.dispose()


def regionSQL():
    #chargement du csv dans un dataframe
    popDep = pd.read_csv("../../data/raw/populationDepartementsFrance.csv", sep=",")

    #création d'un dataframe qui correspond à mon entité
    dfRegion = pd.DataFrame({
        'idRegion' : popDep['codeRegion'],
        'nomRegion' : popDep['nomRegion']
    }).drop_duplicates(subset = ["idRegion"]).set_index("idRegion")
    
    #chargement du dataframe dans le sql
    dataFrameToMySQLTable("Population", "Region", dfRegion)


def departementSQL():
    #chargement du csv dans un dataframe
    popDep = pd.read_csv("../../data/raw/populationDepartementsFrance.csv", sep=",")
    dfDepartement = pd.DataFrame({
        'numeroDepartement' : popDep['codeDepart'],
        'nomDepartement' : popDep['nomDepart'],
        'idRegion' : popDep['codeRegion']
    })

    #gestion de la spécificité de la corse
    ligneA = dfDepartement.iloc[28]
    ligneB = dfDepartement.iloc[29]
    dfDepartement1 = dfDepartement.drop([28,29])
    dfDepartement1 = pd.concat([dfDepartement1[:0], pd.DataFrame([ligneA]), dfDepartement1[0:]])
    dfDepartement1 = pd.concat([dfDepartement1[:20], pd.DataFrame([ligneB]), dfDepartement1[20:]]).reset_index(drop=True)
    
    #création de l'id à partir de l'index
    dfDepartement1.index.names = ["idDepartement"]

    #chargement du dataframe dans le sql
    dataFrameToMySQLTable("Population", "Departement", dfDepartement1)


#création d'une fonction qui transforme le codeGeo en idDepartement
#cette fonction sera utilisé avec la fonction apply de pandas dans la fonction villeSQL
def codeToDep(df):
    df = str(df)
    if (len(df) == 4):
        return int(df[0])
    elif df[:2] in ['97']:
        if df[:3] in ['971']:
            return 96
        elif df[:3] in ['972']:
            return 97
        elif df[:3] in ['973']:
            return 98
        elif df[:3] in ['974']:
            return 99
        elif df[:3] in ['976']:
            return 100
        else:
            print(df)
    elif df[:2] in ['2A']:
        return 0
    elif df[:2] in ['2B']:
        return 20
    else:
        return int(df[:2])

def villeSQL():
    #chargement du csv dans un dataframe
    popMeta = pd.read_csv("../../data/raw/populationMetaDataSerieHistorique2020.csv", sep=";")
    popSerie = pd.read_csv("../../data/raw/populationSerieHistorique2020.csv", sep=";")

    #nettoyage des 30 premières lignes nulles
    dfMetaVille = pd.DataFrame({
        'idVille' : popMeta['COD_MOD'],
        'nomVille' : popMeta['LIB_MOD']
    }).dropna().reset_index()

    #construction de l'idDepartement pour les villes
    dfTmp = pd.DataFrame({'codeGeo' : popSerie['CODGEO']})
    dfTmp['codeGeo'] = dfTmp['codeGeo'].apply(codeToDep)

    #construction le dataframe pour la ville
    dfVille = pd.DataFrame({
        'codeGeo' : popSerie['CODGEO'],
        'superficieVille' : popSerie['SUPERF'],
        'nomVille' : dfMetaVille['nomVille'],
        'idDepartement' : dfTmp['codeGeo']
    })
    dfVille.index.names = ["idVille"]

    #chargement du dataframe dans le sql
    dataFrameToMySQLTable("Population", "Ville", dfVille)

def recenserSQL():
    #chargement du csv dans un dataframe
    popSerie = pd.read_csv("../../data/raw/populationSerieHistorique2020.csv", sep=";")

    #creation des dataframe de recensement par année
    df20 = pd.DataFrame({
        'annee' : 2020,
        'popuplation' : popSerie['P20_POP'],
        'nbLogement' : popSerie['P20_LOG'],
        'nbNaissances' : popSerie['NAIS1420'],
        'nbDeces' : popSerie['DECE1420']
    })
    df20.index.names = ["idVille"]
    
    df14 = pd.DataFrame({
        'annee' : 2014,
        'popuplation' : popSerie['P14_POP'],
        'nbLogement' : popSerie['P14_LOG'],
        'nbNaissances' : popSerie['NAIS0914'],
        'nbDeces' : popSerie['DECE0914']
    })
    df14.index.names = ["idVille"]
    
    df09 = pd.DataFrame({
        'annee' : 2009,
        'popuplation' : popSerie['P09_POP'],
        'nbLogement' : popSerie['P09_LOG'],
        'nbNaissances' : popSerie['NAIS9909'],
        'nbDeces' : popSerie['DECE9909']
    })
    df09.index.names = ["idVille"]
    
    df99 = pd.DataFrame({
        'annee' : 1999,
        'popuplation' : popSerie['D99_POP'],
        'nbLogement' : popSerie['D99_LOG'],
        'nbNaissances' : popSerie['NAIS9099'],
        'nbDeces' : popSerie['DECE9099']
    })
    df99.index.names = ["idVille"]

    df90 = pd.DataFrame({
        'annee' : 1990,
        'popuplation' : popSerie['D90_POP'],
        'nbLogement' : popSerie['D90_LOG'],
        'nbNaissances' : popSerie['NAIS8290'],
        'nbDeces' : popSerie['DECE8290']
    })
    df90.index.names = ["idVille"]

    df82 = pd.DataFrame({
        'annee' : 1982,
        'popuplation' : popSerie['D82_POP'],
        'nbLogement' : popSerie['D82_LOG'],
        'nbNaissances' : popSerie['NAIS7582'],
        'nbDeces' : popSerie['DECE7582']
    })
    df82.index.names = ["idVille"]

    df75 = pd.DataFrame({
        'annee' : 1975,
        'popuplation' : popSerie['D75_POP'],
        'nbLogement' : popSerie['D75_LOG'],
        'nbNaissances' : popSerie['NAIS6875'],
        'nbDeces' : popSerie['DECE6875']
    })
    df75.index.names = ["idVille"]

    df68 = pd.DataFrame({
        'annee' : 1968,
        'popuplation' : popSerie['D68_POP'],
        'nbLogement' : popSerie['D68_LOG'],
    })
    df68.index.names = ["idVille"]

    #chargement des dataframe dans le sql
    dataFrameToMySQLTable("Population", "Recenser", df20)
    dataFrameToMySQLTable("Population", "Recenser", df14)
    dataFrameToMySQLTable("Population", "Recenser", df09)
    dataFrameToMySQLTable("Population", "Recenser", df99)
    dataFrameToMySQLTable("Population", "Recenser", df90)
    dataFrameToMySQLTable("Population", "Recenser", df82)
    dataFrameToMySQLTable("Population", "Recenser", df75)
    dataFrameToMySQLTable("Population", "Recenser", df68)
