# Projet BDD Population - Recensements Français INSEE (1968-2020)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

## Description

Base de données MySQL pour analyser l'évolution de la population française sur plus de 50 ans (1968-2020). Projet réalisé dans le cadre du Master 1 MACIA - Programmation Analyse.

### Fonctionnalités principales
- Import automatisé des données INSEE via Python/Pandas
- 19 requêtes SQL analytiques (questions a-i + 5 inventées)
- Gestion des cas particuliers (Corse 2A/2B, DOM-TOM 971-976)
- Visualisations graphiques avec Matplotlib

## Démarrage rapide

### Prérequis
- MySQL 8.0+
- Python 3.11+
- pip

### Installation

```bash
# 1. Cloner le projet
git clone <url-du-repo>

# 2. Créer le fichier de mot de passe MySQL
echo "votre_mot_de_passe" > src/python/mdp.txt

# 3. Installer les dépendances
pip install mysql-connector-python pandas sqlalchemy matplotlib
```

### Utilisation

```bash
# Lancer le script principal (tout est automatisé)
cd src/python
python main.py
```

## Structure du projet

```
Projet_PGA/
├── src/python/
│   ├── main.py              # Script principal (point d'entrée)
│   ├── connexion.py         # Gestion connexion MySQL
│   ├── creationBDD.py       # Création BDD + import CSV
│   ├── requetes.py          # 19 fonctions SQL
│   └── graphique.py         # Génération graphiques
├── sql/
│   ├── creationBDD.sql      # Schéma relationnel complet
│   └── requetesRecensement.sql  # Toutes les requêtes SQL
├── graphiques/              # PNG générés
├── data/                    # Données CSV INSEE
└── README.md
```

## Fonctionnalités détaillées

### Requêtes implémentées
- **a-i)** Questions originales : population, évolution, croissance, naissances, décès, densité
- **5 requêtes inventées)** GROUP BY, sous-requêtes, WITH clauses, JOIN avancés

### Cas particuliers gérés
- **Corse** : Codes 2A/2B → IDs 0 et 20
- **DOM-TOM** : Codes 971-976 → IDs 96-100
- **Paris** : Gestion ville vs arrondissements via vues SQL

## Schéma de la base

```
Region (idRegion PK, nomRegion)
    ↑
Departement (idDepartement PK, numeroDepartement, nomDepartement, idRegion FK)
    ↑
Ville (idVille PK, codeGeo, superficieVille, nomVille, idDepartement FK)
    ↑
Recenser (idVille PK, annee PK, population, nbLogement, nbNaissances, nbDeces)
```

## Auteurs

- **BONICEL Basile**
- **DUCARUGE Oscar** 
- **JIENU Bryan**

Master 1 MACIA - CY Cergy Paris Université (2025-2026)  
Encadrant : VERIN RENAUD
