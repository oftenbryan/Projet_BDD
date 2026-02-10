import matplotlib.pyplot as plt
import pandas as pd
from connexion import connexionBDD
from requetes import requete_b


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


if __name__ == "__main__":
    cnx = connexionBDD()
    graph_evolution_france(cnx)
    plt.close("all")
