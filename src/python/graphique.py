import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from connexion import *
from requetes import *



def graph_evolution_france(cnx):
    #chargement du résultat de la requete dans un dataframe
    df = pd.read_sql(requete_b(), cnx)

    #creation du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(
        df["annee"],
        df["populationFrance"] / 1000000,
        marker="o",
        linewidth=2,
        color="blue",
    )
    plt.title("Evolution de la population francaise (1968-2020)", fontsize=14)
    plt.xlabel("Annee")
    plt.ylabel("Population (millions)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("../../graphiques/evolution_france.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique evolution_france.png cree ")

def graph_pop_region(cnx):
    #chargement du résultat de la requete dans un dataframe
    df = pd.read_sql(requete_c_region(), cnx)

    #creation du graphique
    plt.figure(figsize=(10, 6))
    plt.bar(
        df["nomReg"],
        df["populationReg"] / 1000000,
        color="skyblue",
    )
    plt.title("Population française par région (2020)", fontsize=14)
    plt.xlabel("Region")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Population (millions)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    #sauvegarde du graphique dans le dossier graphiques
    plt.savefig("../../graphiques/pop_region.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique pop_region.png cree ")

def graph_croissance_ville(cnx):
    #chargement du résultat de la requete dans un dataframe
    df = pd.read_sql(requete_e_villes(), cnx)

    #creation du graphique
    plt.figure(figsize=(10, 6))
    plt.bar(
        df["nomVille"],
        df["croissanceVille"],
        color="skyblue",
    )
    plt.title("Top 10 des villes à la croissance la plus rapide (1968-2020)", fontsize=14)
    plt.xlabel("Villes")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Augmentation de population")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    #sauvegarde du graphique dans le dossier graphiques
    plt.savefig("../../graphiques/top10_croissance_ville.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique top10_croissance_ville.png cree ")

def graph_naissances_ville(cnx):
    #chargement du résultat de la requete dans un dataframe
    df = pd.read_sql(requete_f_naissance_villes(), cnx)

    #creation du graphique
    plt.figure(figsize=(10, 6))
    plt.bar(
        df["nomVille"],
        df["totalNaissances"] / 1000,
        color="skyblue",
    )
    plt.title("Top 10 des villes avec le plus de naissance (1968-2020)", fontsize=14)
    plt.xlabel("Villes")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Nombre de naissance (milliers)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    #sauvegarde du graphique dans le dossier graphiques
    plt.savefig("../../graphiques/top10_naissance_ville.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique top10_naissance_ville.png cree ")

def graph_densite_ville(cnx):
    #chargement du résultat de la requete dans un dataframe
    df = pd.read_sql(requete_g_villes_grande(), cnx)

    #creation du graphique
    plt.figure(figsize=(10, 6))
    plt.bar(
        df["nomVille"],
        df["densitePop"],
        color="skyblue",
    )
    plt.title("Top 10 des villes avec la plus grande densité", fontsize=14)
    plt.xlabel("Villes")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Densité")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    #sauvegarde du graphique dans le dossier graphiques
    plt.savefig("../../graphiques/top10_densite_ville.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique top10_densite_ville.png cree ")

def graph_mvt_pop(cnx):
    #chargement du résultat de la requete dans un dataframe
    df = pd.read_sql(requete_i(), cnx)

    #preparation des labels
    labels = df['annee'].astype(str)

    #extraction des données
    naissances = df["naissances"].fillna(0) / 1000000
    deces = df["deces"].fillna(0) / 1000000
    population = df["mouvements"].fillna(0) / 100000

    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    # création des trois barres
    rects1 = ax.bar(x - width, naissances, width, label='Naissances', color='#3498db')
    rects2 = ax.bar(x, deces, width, label='Décès', color='#e74c3c')
    rects3 = ax.bar(x + width, population, width, label='Mouvement de population', color='#2ecc71')

    # configuration des axes
    ax.set_ylabel("Naissance/Deces (millions) - Mouvement (milliers)")
    ax.set_xlabel("Année")
    ax.set_title("Evolution de population (1968-2020)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    #sauvegarde du graphique dans le dossier graphiques
    plt.savefig("../../graphiques/mvt_pop.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique mvt_pop.png cree ")



if __name__ == "__main__":
    cnx = connexionBDD()
    graph_evolution_france(cnx)
    plt.close("all")
