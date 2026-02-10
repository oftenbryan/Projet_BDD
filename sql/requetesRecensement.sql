USE Population;

DROP VIEW IF EXISTS villeSeule;
DROP VIEW IF EXISTS arrondissement;

-- Création des vues villeSeule et arrondissement afin de séparer la table ville en deux tables.
-- On facilite ainsi les calculs de population et on évite les valeurs comptées en double.
CREATE VIEW villeSeule AS (
	SELECT *
	FROM ville
	WHERE LOWER(nomVille) NOT LIKE "%arrondissement"
);

CREATE VIEW arrondissement AS (
	SELECT *
	FROM ville
	WHERE LOWER(nomVille) LIKE "%arrondissement"
);


-- Vérifications de la bonne création des vues statiques
SELECT * FROM arrondissement;
SELECT * FROM villeSeule WHERE nomVille LIKE "Paris%";


-- 1. Réaliser les requêtes suivantes :


-- a. Liste des populations en 2020 avec le nom de ville, département, région.

SELECT rcs.population, vs.nomVille, d.nomDepartement, reg.nomRegion
FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
				  JOIN Departement d ON vs.idDepartement = d.idDepartement
                  JOIN Region reg ON d.idRegion = reg.idRegion
WHERE rcs.annee = 2020
ORDER BY population DESC;


-- b. Évolution de la population française de 1968 à 2020.

SELECT rcs.annee, SUM(rcs.population) populationFrance
FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
GROUP BY rcs.annee;


-- c. Liste des populations en 2020 par département / région avec leurs noms (2 requêtes).

-- Par département :

SELECT d.idDepartement idDep, d.nomDepartement nomDep, SUM(rcs.population) populationDep
FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
				  JOIN Departement d ON vs.idDepartement = d.idDepartement
WHERE rcs.annee = 2020
GROUP BY idDep, nomDep
ORDER BY populationDep DESC;


-- Par région :

SELECT reg.idRegion idReg, reg.nomRegion nomReg, SUM(rcs.population) populationReg
FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
				  JOIN Departement d ON vs.idDepartement = d.idDepartement
				  JOIN Region reg ON d.idRegion = reg.idRegion
WHERE rcs.annee = 2020
GROUP BY idReg, nomReg
ORDER BY populationReg DESC;


-- d. Population de Paris au total et par arrondissement. Quel est le problème ? Corriger et vérifier que ce cas n’est pas produit ailleurs. Revoir la question 2.

SELECT rcs.population populationParis
FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
WHERE annee = 2020 AND LOWER(vs.nomVille) LIKE "paris";

SELECT SUM(rcs.population) populationParis
FROM Recenser rcs JOIN arrondissement a ON rcs.idVille = a.idVille
WHERE annee = 2020 AND LOWER(a.nomVille) LIKE "paris%";


-- e. Liste des 10 villes / départements / régions ayant cru le plus de 1968 à 2020.

-- Pour les villes : 

-- TODO : WITH en amont pour pas recalculer le SELECT deux fois identiques pour deux WHERE différents ensuite
WITH population2020 AS (
		SELECT vs.idVille idVille, vs.nomVille nomVille, rcs.population popVille
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
        WHERE rcs.annee = 2020
        ),
	population1968 AS (
		SELECT vs.idVille idVille, vs.nomVille nomVille, rcs.population popVille
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
        WHERE rcs.annee = 1968
        )

SELECT pop20.nomVille, (pop20.popVille - pop68.popVille) croissanceVille
FROM population2020 pop20 JOIN population1968 pop68 ON pop20.idVille = pop68.idVille
ORDER BY croissanceVille DESC LIMIT 10;


-- Pour les départements :

-- TODO : same as above
WITH popDep2020 AS (
		SELECT d.idDepartement idDep, d.nomDepartement nomDep, SUM(rcs.population) popDep
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
						  JOIN Departement d ON vs.idDepartement = d.idDepartement
        WHERE rcs.annee = 2020
        GROUP BY idDep, nomDep
        ),
	popDep1968 AS (
		SELECT d.idDepartement idDep, d.nomDepartement nomDep, SUM(rcs.population) popDep
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
						  JOIN Departement d ON vs.idDepartement = d.idDepartement
        WHERE rcs.annee = 1968
        GROUP BY idDep, nomDep
        )

SELECT d20.nomDep, (d20.popDep - d68.popDep) croissanceDep
FROM popDep2020 d20 JOIN popDep1968 d68 ON d20.idDep = d68.idDep
ORDER BY croissanceDep DESC LIMIT 10;


-- Pour les régions :

-- TODO : same as above
WITH popReg2020 AS (
		SELECT reg.idRegion idRegion, reg.nomRegion nomRegion, SUM(rcs.population) popRegion
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
						  JOIN Departement d ON vs.idDepartement = d.idDepartement
                          JOIN Region reg ON d.idRegion = reg.idRegion
        WHERE rcs.annee = 2020
        GROUP BY idRegion, nomRegion
        ),
	popReg1968 AS (
		SELECT reg.idRegion idRegion, reg.nomRegion nomRegion, SUM(rcs.population) popRegion
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille
						  JOIN Departement d ON vs.idDepartement = d.idDepartement
                          JOIN Region reg ON d.idRegion = reg.idRegion
        WHERE rcs.annee = 1968
        GROUP BY idRegion, nomRegion
        ),
	croissanceReg AS (

SELECT r20.nomRegion, (r20.popRegion - r68.popRegion) croissanceRegion
FROM popReg2020 r20 JOIN popReg1968 r68 ON r20.idRegion = r68.idRegion
ORDER BY croissanceRegion DESC) -- LIMIT 10

SELECT SUM(cr.croissanceRegion) croissanceFr FROM croissanceReg cr;
-- Note pour reprendre : j'obtiens 16 364 042 ici, alors que par Wiki je trouve 17 718 778. ça fait quand même une diff de 1,5 million d'habitants, wtf.
-- TODO : La différence de valeur est vraiment importante. À réétudier.

-- f. Liste des 10 villes / départements où on nait / meurt le plus.



-- g. Liste des 10 villes / départements avec la plus grande/petite densité.



-- h. Comparaison pour 2020 des naissances / décès / mouvements de population par
-- département / région (2 requêtes). (Mouvements =deltapop(1968/2020)-(nais-deces)).



-- i. Comparaison par recensement des naissances / décès / mouvements de population de
-- la France.


