import datetime
import mysql.connector
from connexion import *
from import_data import *
from requetes import *
from graphique import *


def main():

    #création du connecteur
    cnx = connexionBDD()

    #test pour éviter de recréer la base de données à chaque exéctution du main
    firstCo = input("Voulez vous (re)créer la base de donée à partir des csv ? (y/n)")
    if (firstCo == 'y'):
        creer_bdd(cnx)
        regionSQL()
        departementSQL()
        villeSQL()
        recenserSQL()

    #préparation du sql
    usePopulation(cnx)
    vues(cnx)


    #requêtes de la question 1) avec d'éventuelles créations de graphiques
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
    graph_croissance_ville(cnx)

    print("\n" + "=" * 60)
    print("e) Top 10 departements par croissance")
    afficher_resultat(requeteSimple(cnx, requete_e_departements()))

    print("\n" + "=" * 60)
    print("e) Top 10 regions par croissance")
    afficher_resultat(requeteSimple(cnx, requete_e_region()))

    print("\n" + "=" * 60)
    print("f) Top 10 villes naissances")
    afficher_resultat(requeteSimple(cnx, requete_f_naissance_villes()))
    graph_naissances_ville(cnx)

    print("\n" + "=" * 60)
    print("f) Top 10 villes deces")
    afficher_resultat(requeteSimple(cnx, requete_f_deces_villes()))

    print("\n" + "=" * 60)
    print("f) Top 10 departements naissances")
    afficher_resultat(requeteSimple(cnx, requete_f_naissance_departements()))

    print("\n" + "=" * 60)
    print("f) Top 10 departements deces")
    afficher_resultat(requeteSimple(cnx, requete_f_deces_departements()))

    print("\n" + "=" * 60)
    print("g) Top 10 villes - plus grande densite")
    afficher_resultat(requeteSimple(cnx, requete_g_villes_grande()))
    graph_densite_ville(cnx)

    print("\n" + "=" * 60)
    print("g) Top 10 villes - plus petite densite")
    afficher_resultat(requeteSimple(cnx, requete_g_villes_petite()))

    print("\n" + "=" * 60)
    print("g) Top 10 departements - plus grande densite")
    afficher_resultat(requeteSimple(cnx, requete_g_departements_grande()))

    print("\n" + "=" * 60)
    print("g) Top 10 departements - plus petite densite")
    afficher_resultat(requeteSimple(cnx, requete_g_departements_petite()))

    print("\n" + "=" * 60)
    print("h) Comparaison 2020 - naissances, deces, mouvements par departement")
    afficher_resultat(requeteSimple(cnx, requete_h_departement()), 20)

    print("\n" + "=" * 60)
    print("h) Comparaison 2020 - naissances, deces, mouvements par region")
    afficher_resultat(requeteSimple(cnx, requete_h_region()))
    graph_pop_over_avg(cnx)

    print("\n" + "=" * 60)
    print("i) Comparaison France par recensement")
    afficher_resultat(requeteSimple(cnx, requete_i()))
    #graph_mvt_pop(cnx)

    #requetes de la question 2) avec d'éventuelles créations de graphiques
    print("\n" + "=" * 60)
    print("1) Donner le nombre de villes en Normandie")
    afficher_resultat(requeteSimple(cnx, requete_1()))

    print("\n" + "=" * 60)
    print("2) Donner les villes de la Creuse qui sont plus peuplées que la moyenne des communes françaises en 2020")
    afficher_resultat(requeteSimple(cnx, requete_2()))

    print("\n" + "=" * 60)
    print("3) Donner les 10 villes qui ont vu le plus grand pourcentage de décès par rapport à leur population entre 2014 et 2020.")
    afficher_resultat(requeteSimple(cnx, requete_3()))

    #fin de la connexion à la base de données
    fermerCnx(cnx)


if __name__ == "__main__":
    main()
