import datetime
import mysql.connector
from connexion import connexionBDD, selectDB, fermerCnx
from import_data import regionSQL, departementSQL, villeSQL, recenserSQL
from requetes import (
    creer_bdd,
    usePopulation,
    vues,
    requete_a,
    requete_b,
    requete_c_departement,
    requete_c_region,
    requete_d_paris,
    requete_e_villes,
    requete_e_departements,
    requete_f,
    requete_g,
    requete_h,
    requete_i,
)


def main():
    # Connexion a MySQL
    cnx = connexionBDD()

    # Creation de la base de donnees et des tables
    creer_bdd(cnx)
    regionSQL()
    departementSQL()
    villeSQL()
    recenserSQL()

    # Selection de la base de donnees
    usePopulation(cnx)

    # Creation des vues
    vues(cnx)

    # ============================================================
    # APPEL DES REQUETES
    # ============================================================

    print("=" * 60)
    print("a) Liste des populations en 2020 (ville, departement, region)")
    requete_a(cnx)

    print("\n" + "=" * 60)
    print("b) Evolution de la population francaise (1968-2020)")
    requete_b(cnx)

    print("\n" + "=" * 60)
    print("c) Populations 2020 par departement")
    requete_c_departement(cnx)

    print("\n" + "=" * 60)
    print("c) Populations 2020 par region")
    requete_c_region(cnx)

    print("\n" + "=" * 60)
    print("d) Population de Paris (ville + arrondissements)")
    requete_d_paris(cnx)

    print("\n" + "=" * 60)
    print("e) Top 10 des villes ayant le plus grandi (1968-2020)")
    requete_e_villes(cnx)

    print("\n" + "=" * 60)
    print("e) Top 10 des departements ayant le plus grandi (1968-2020)")
    requete_e_departements(cnx)

    print("\n" + "=" * 60)
    print("f) Top 10 villes/departements naissances/deces (TODO)")
    requete_f(cnx)

    print("\n" + "=" * 60)
    print("g) Densite de population (TODO)")
    requete_g(cnx)

    print("\n" + "=" * 60)
    print("h) Comparaison 2020 naissances/deces/mouvements (TODO)")
    requete_h(cnx)

    print("\n" + "=" * 60)
    print("i) Comparaison par recensement France (TODO)")
    requete_i(cnx)

    # Fermeture de la connexion
    fermerCnx(cnx)


if __name__ == "__main__":
    main()
