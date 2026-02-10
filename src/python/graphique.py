import matplotlib.pyplot as plt
import pandas as pd
from connexion import connexionBDD
from requetes import (
    requete_b,
    requete_c_region,
    requete_e_villes,
    requete_f_naissance_villes
)



def graph_evolution_france(cnx):
    """Line chart - Evolution de la population francaise 1968-2020"""
    df = pd.read_sql(requete_b(), cnx)
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
    df = pd.read_sql(requete_c_region(), cnx)
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
    plt.savefig("../../graphiques/pop_region.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique pop_region.png cree ")

def graph_croissance_ville(cnx):
    df = pd.read_sql(requete_e_villes(), cnx)
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
    plt.savefig("../../graphiques/top10_croissance_ville.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique top10_croissance_ville.png cree ")

def graph_naissances_ville(cnx):
    df = pd.read_sql(requete_f_naissance_villes(), cnx)
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
    plt.savefig("../../graphiques/top10_naissance_ville.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Graphique top10_naissance_ville.png cree ")


if __name__ == "__main__":
    cnx = connexionBDD()
    graph_evolution_france(cnx)
    plt.close("all")
