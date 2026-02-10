import datetime
import mysql.connector
from connexion import connexionBDD, selectDB, fermerCnx
from import_data import regionSQL, departementSQL, villeSQL, recenserSQL
from requetes import (
    creer_bdd,
    usePopulation,
    vues,
    requeteSimple,
    afficher_resultat,
    requete_a,
    requete_b,
    requete_c_departement,
    requete_c_region,
    requete_d_paris,
    requete_e_villes,
    requete_e_departements,
    requete_e_region,
)
from graphique import graph_evolution_france, graph_pop_region


def main():
    cnx = connexionBDD()
    #creer_bdd(cnx)
    #regionSQL()
    #departementSQL()
    #villeSQL()
    #recenserSQL()
    usePopulation(cnx)
    vues(cnx)

    print("=" * 60)
    print("a) Liste des populations en 2020")
    requete_a(cnx)

    print("\n" + "=" * 60)
    print("b) Evolution population (1968-2020)")
    afficher_resultat(requeteSimple(cnx, requete_b()))
    graph_evolution_france(cnx)

    print("\n" + "=" * 60)
    print("c) Populations 2020 par departement")
    requete_c_departement(cnx)

    print("\n" + "=" * 60)
    print("c) Populations 2020 par region")
    afficher_resultat(requeteSimple(cnx, requete_c_region()))
    graph_pop_region(cnx)

    print("\n" + "=" * 60)
    print("d) Population de Paris")
    requete_d_paris(cnx)

    print("\n" + "=" * 60)
    print("e) Top 10 villes croissance")
    requete_e_villes(cnx)

    print("\n" + "=" * 60)
    print("e) Top 10 departements croissance")
    requete_e_departements(cnx)

    fermerCnx(cnx)


if __name__ == "__main__":
    main()
