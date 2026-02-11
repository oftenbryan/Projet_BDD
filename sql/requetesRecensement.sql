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
        )

SELECT r20.nomRegion, (r20.popRegion - r68.popRegion) croissanceRegion
FROM popReg2020 r20 JOIN popReg1968 r68 ON r20.idRegion = r68.idRegion
ORDER BY croissanceRegion DESC LIMIT 10;

-- f. Liste des 10 villes / départements où on nait / meurt le plus.

-- Villes où on meurt le plus (total sur toute la période)
SELECT 
	vs.nomVille, 
    d.nomDepartement,
    SUM(rcs.nbDeces) as totalDeces
FROM Recenser rcs 
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
    JOIN Departement d ON vs.idDepartement = d.idDepartement
GROUP BY vs.idVille, vs.nomVille, d.nomDepartement
ORDER BY totalDeces DESC LIMIT 10;

-- Villes où on naît le plus (total sur toute la période)
SELECT 
	vs.nomVille, 
    d.nomDepartement,
    SUM(rcs.nbNaissances) as totalNaissances
FROM Recenser rcs 
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
	JOIN Departement d ON vs.idDepartement = d.idDepartement
GROUP BY vs.idVille, vs.nomVille, d.nomDepartement
ORDER BY totalNaissances DESC LIMIT 10;

-- Départements où on meurt le plus
SELECT 
    d.nomDepartement,
    SUM(rcs.nbDeces) as totalDeces
FROM Recenser rcs 
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
    JOIN Departement d ON vs.idDepartement = d.idDepartement
GROUP BY d.idDepartement, d.nomDepartement
ORDER BY totalDeces DESC LIMIT 10;

-- Départements où on naît le plus
SELECT 
    d.nomDepartement,
    SUM(rcs.nbNaissances) as totalNaissances
FROM Recenser rcs 
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
    JOIN Departement d ON vs.idDepartement = d.idDepartement
GROUP BY d.idDepartement, d.nomDepartement
ORDER BY totalNaissances DESC LIMIT 10;

-- g. Liste des 10 villes / départements avec la plus grande/petite densité.

-- Villes avec la plus grande densité
SELECT
	vs.nomVille,
	d.nomDepartement,
	AVG(rcs.population) / vs.superficieVille AS densitePop
FROM Recenser rcs
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
	JOIN Departement d ON vs.idDepartement = d.idDepartement
WHERE vs.superficieVille > 0
GROUP BY vs.idVille, vs.nomVille, d.nomDepartement, vs.superficieVille
ORDER BY densitePop DESC
LIMIT 10;

-- Villes avec la plus petite densité
SELECT
	vs.nomVille,
	d.nomDepartement,
	AVG(rcs.population) / vs.superficieVille AS densitePop
FROM Recenser rcs
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
	JOIN Departement d ON vs.idDepartement = d.idDepartement
WHERE vs.superficieVille > 0
GROUP BY vs.idVille, vs.nomVille, d.nomDepartement, vs.superficieVille
ORDER BY densitePop ASC
LIMIT 10;

-- Départements avec la plus grande densité
SELECT
	d.nomDepartement,
	SUM(rcs.population) / SUM(vs.superficieVille) AS densitePop
FROM Recenser rcs
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
	JOIN Departement d ON vs.idDepartement = d.idDepartement
WHERE vs.superficieVille > 0
GROUP BY d.idDepartement, d.nomDepartement
ORDER BY densitePop DESC
LIMIT 10;

-- Départements avec la plus petite densité
SELECT
	d.nomDepartement,
	SUM(rcs.population) / SUM(vs.superficieVille) AS densitePop
FROM Recenser rcs
	JOIN villeSeule vs ON rcs.idVille = vs.idVille
	JOIN Departement d ON vs.idDepartement = d.idDepartement
WHERE vs.superficieVille > 0
GROUP BY d.idDepartement, d.nomDepartement
ORDER BY densitePop ASC
LIMIT 10;

-- h. Comparaison pour 2020 des naissances / décès / mouvements de population par
-- département / région (2 requêtes). (Mouvements =deltapop(1968/2020)-(nais-deces)).

WITH stats1968Dpt AS (
    SELECT d.idDepartement, d.nomDepartement,
           SUM(rcs.population) AS pop1968,
           SUM(rcs.nbNaissances) AS nais1968,
           SUM(rcs.nbDeces) AS deces1968
    FROM Recenser rcs
    JOIN villeSeule vs ON rcs.idVille = vs.idVille
    JOIN Departement d ON vs.idDepartement = d.idDepartement
    WHERE rcs.annee = 1968
    GROUP BY d.idDepartement, d.nomDepartement
),
stats2020Dpt AS (
    SELECT d.idDepartement, d.nomDepartement,
           SUM(rcs.population) AS pop2020,
           SUM(rcs.nbNaissances) AS nais2020,
           SUM(rcs.nbDeces) AS deces2020
    FROM Recenser rcs
    JOIN villeSeule vs ON rcs.idVille = vs.idVille
    JOIN Departement d ON vs.idDepartement = d.idDepartement
    WHERE rcs.annee = 2020
    GROUP BY d.idDepartement, d.nomDepartement
)
SELECT
    s20.nomDepartement,
    s20.nais2020 AS naissances,
    s20.deces2020 AS deces,
    (s20.pop2020 - s68.pop1968) AS deltaPop,
    (s20.pop2020 - s68.pop1968) - (s20.nais2020 - s20.deces2020) AS mouvements
FROM stats2020Dpt s20
JOIN stats1968Dpt s68 ON s20.idDepartement = s68.idDepartement;


-- h. Par région :
WITH stats1968Reg AS (
    SELECT reg.idRegion, reg.nomRegion,
           SUM(rcs.population) AS pop1968,
           SUM(rcs.nbNaissances) AS nais1968,
           SUM(rcs.nbDeces) AS deces1968
    FROM Recenser rcs
    JOIN villeSeule vs ON rcs.idVille = vs.idVille
    JOIN Departement d ON vs.idDepartement = d.idDepartement
    JOIN Region reg ON d.idRegion = reg.idRegion
    WHERE rcs.annee = 1968
    GROUP BY reg.idRegion, reg.nomRegion
),
stats2020Reg AS (
    SELECT reg.idRegion, reg.nomRegion,
           SUM(rcs.population) AS pop2020,
           SUM(rcs.nbNaissances) AS nais2020,
           SUM(rcs.nbDeces) AS deces2020
    FROM Recenser rcs
    JOIN villeSeule vs ON rcs.idVille = vs.idVille
    JOIN Departement d ON vs.idDepartement = d.idDepartement
    JOIN Region reg ON d.idRegion = reg.idRegion
    WHERE rcs.annee = 2020
    GROUP BY reg.idRegion, reg.nomRegion
)
SELECT
    s20.nomRegion,
    s20.nais2020 AS naissances,
    s20.deces2020 AS deces,
    (s20.pop2020 - s68.pop1968) AS deltaPop,
    (s20.pop2020 - s68.pop1968) - (s20.nais2020 - s20.deces2020) AS mouvements
FROM stats2020Reg s20
JOIN stats1968Reg s68 ON s20.idRegion = s68.idRegion;


-- i. Comparaison par recensement des naissances / décès / mouvements de population de
-- la France. (Mouvements = deltaPop - (naissances - décès))

WITH stats AS (
    SELECT 
        rcs.annee,
        SUM(rcs.population) AS population,
        SUM(rcs.nbNaissances) AS naissances,
        SUM(rcs.nbDeces) AS deces
    FROM Recenser rcs
    JOIN villeSeule vs ON rcs.idVille = vs.idVille
    GROUP BY rcs.annee
)
SELECT 
    annee,
    naissances,
    deces,
    population - LAG(population) OVER (ORDER BY annee) AS deltaPop,
    (population - LAG(population) OVER (ORDER BY annee)) - (naissances - deces) AS mouvements
FROM stats
ORDER BY annee;


-- 3.

WITH deces AS (
		SELECT vs.idVille, vs.nomVille, rcs.nbDeces
		FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille AND rcs.annee = 2020
	),
    pop2014 AS (
		SELECT vs.idVille, vs.nomVille, rcs.population population
        FROM Recenser rcs JOIN villeSeule vs ON rcs.idVille = vs.idVille AND rcs.annee = 2014
	)

SELECT (d.nbDeces / p14.population) ratioDeces, d.nomVille
FROM deces d JOIN pop2014 p14 ON d.idVille = p14.idVille
ORDER BY ratioDeces DESC LIMIT 10;


-- 4. TOP 10 Villes DOM-TOM par population 1990

SELECT vs.nomVille, rcs.population
FROM villeSeule vs
JOIN Departement d ON vs.idDepartement = d.idDepartement
JOIN Recenser rcs ON vs.idVille = rcs.idVille AND rcs.annee = 1990
WHERE d.numeroDepartement LIKE '97%'
ORDER BY rcs.population DESC
LIMIT 10;


-- 5.
