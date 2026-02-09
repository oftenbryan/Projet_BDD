USE Population;

CREATE VIEW villeSeule AS (
	SELECT *
	FROM ville
	WHERE nomVille NOT LIKE "%Arrondissement"
);

CREATE VIEW arrondissement AS (
	SELECT *
	FROM ville
	WHERE nomVille LIKE "%Arrondissement"
);

-- Vérifications de la bonne création des vues statiques
SELECT * FROM arrondissement;
SELECT * FROM villeSeule WHERE nomVille LIKE "Paris%";

-- 1. Réaliser les requêtes suivantes :

-- a. Liste des populations en 2020 avec le nom de ville, département, région.

SELECT rcs.population, vs.nomVille, d.nomDepartement, reg.nomRegion
FROM Recenser rcs JOIN villeseule vs ON rcs.idVille = vs.idVille
				  JOIN Departement d ON vs.idDepartement = d.idDepartement
                  JOIN Region reg ON d.idRegion = reg.idRegion
WHERE rcs.annee = 2020
ORDER BY population DESC;

-- b. Évolution de la population française de 1968 à 2020.

SELECT rcs.annee, SUM(rcs.population) populationFrance
FROM recenser rcs JOIN villeseule vs ON rcs.idVille = vs.idVille
GROUP BY rcs.annee;

-- c. Liste des populations en 2020 par département / région avec leurs noms (2 requêtes).

SELECT d.idDepartement idDep, d.nomDepartement nomDep, SUM(rcs.population) populationDep
FROM recenser rcs JOIN villeseule vs ON rcs.idVille = vs.idVille
				  JOIN Departement d ON vs.idDepartement = d.idDepartement
WHERE rcs.annee = 2020
GROUP BY idDep, nomDep
ORDER BY populationDep DESC;

SELECT reg.nomRegion, SUM(rcs.population) populationDepartement
FROM recensement rcs JOIN Ville v ON rcs.idVille = v.idVille
					 JOIN Departement d ON v.idDepartement = d.idDepartement
                     JOIN Region reg ON v.idRegion = reg.idRegion
GROUP BY rg.nomRegion;


-- d. Population de Paris au total et par arrondissement. Quel est le problème ? Corriger et
-- vérifier que ce cas n’est pas produit ailleurs. Revoir la question 2.



-- e. Liste des 10 villes / départements / régions ayant cru le plus de 1968 à 2020.



-- f. Liste des 10 villes / départements où on nait / meurt le plus.



-- g. Liste des 10 villes / départements avec la plus grande/petite densité.



-- h. Comparaison pour 2020 des naissances / décès / mouvements de population par
-- département / région (2 requêtes). (Mouvements =deltapop(1968/2020)-(nais-deces)).



-- i. Comparaison par recensement des naissances / décès / mouvements de population de
-- la France.


