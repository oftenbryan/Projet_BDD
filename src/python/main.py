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
    requete_d_paris_ville,
    requete_d_paris_arr,
    requete_e_villes,
    requete_e_departements,
    requete_e_region,
    requete_f_naissance,
    requete_f_deces,
    requete_g,
    requete_h,
    requete_i,
)
from graphique import graph_evolution_france, graph_pop_region


def main():
    cnx = connexionBDD()
    # creer_bdd(cnx)
    # regionSQL()
    # departementSQL()
    # villeSQL()
    # recenserSQL()
    usePopulation(cnx)
    vues(cnx)

    print("=" * 60)
    print("a) Liste des populations en 2020")
    afficher_resultat(requeteSimple(cnx, requete_a()), n=20)

    print("\n" + "=" * 60)
    print("b) Evolution population (1968-2020)")
    afficher_resultat(requeteSimple(cnx, requete_b()))
    graph_evolution_france(cnx)

    print("\n" + "=" * 60)
    print("c) Populations 2020 par departement")
    afficher_resultat(requeteSimple(cnx, requete_c_departement()), n=20)

    print("\n" + "=" * 60)
    print("c) Populations 2020 par region")
    afficher_resultat(requeteSimple(cnx, requete_c_region()))
    graph_pop_region(cnx)

    print("\n" + "=" * 60)
    print("d) Population de Paris")
    print("\n--- Paris (ville) ---")
    afficher_resultat(requeteSimple(cnx, requete_d_paris_ville()))
    print("\n--- Paris (arrondissements) ---")
    afficher_resultat(requeteSimple(cnx, requete_d_paris_arr()))

    print("\n" + "=" * 60)
    print("e) Top 10 villes par croissance")
    afficher_resultat(requeteSimple(cnx, requete_e_villes()))

    print("\n" + "=" * 60)
    print("e) Top 10 departements par croissance")
    afficher_resultat(requeteSimple(cnx, requete_e_departements()))

    print("\n" + "=" * 60)
    print("e) Top 10 regions par croissance")
    afficher_resultat(requeteSimple(cnx, requete_e_region()))

    print("\n" + "=" * 60)
    print("f) Top 10 villes naissances")
    afficher_resultat(requeteSimple(cnx, requete_f_naissance()))

    print("\n" + "=" * 60)
    print("f) Top 10 villes deces")
    afficher_resultat(requeteSimple(cnx, requete_f_deces()))

    print("\n" + "=" * 60)
    print("g) Densite (TODO)")
    print(requete_g())

    print("\n" + "=" * 60)
    print("h) Comparaison 2020 (TODO)")
    print(requete_h())

    print("\n" + "=" * 60)
    print("i) Comparaison France (TODO)")
    print(requete_i())

    fermerCnx(cnx)


if __name__ == "__main__":
    main()
