# Salt creeping

## Premier code de cristallisation

### Objectif, méthode et hypothèses

L'objectif de ce premier code est de simuler la cristallisation en supposant qu'à chaque pas de temps un certain nombre d'ions doit se critalliser. Pour cela, on se place sur une grille (objet avec une matrice de case...). Sur cette grille chaque case (objet avec un type...) possède un type : 

- -2 représente le solide sur lequel les cristaux se forment.
- -1 représente l'air (pas encore utilisé dans cette version, on suppose qu'il y a de l'eau de partout pour l'instant)
- 0 représente l'eau
- Un entier strictement positif représente un des cristaux.

Une première passe de la grille permet de déterminer où les prochains NaCl peuvent se former. Pour cela on fixe les règles suivantes : 

- Si la case est à plus de 2 cases de tout solide la cristallisation ne peut pas se produire.
- Si la case est à une case de distance d'un cristal elle peut former un nouveau cristal.
- Si la case est en contact avec un cristal déjà existant, elle peut le prolonger. 

On ne donne pas la probabilité qu'une case est un cristal directement. On estime plutot le nombre de case où peuvent se former les critaux et on fait le rapport avec le nombre de cistaux disponible. La seul donné importante devient la probabilité qu'un nouveau cristal se forme par rapport à ce qu'un cristal se prolonge simplement.

### Résultats
![](Exp_1_creeping.jpeg)
![](Modèle_1_creeping.png)

### Discussion
On observe que dans l'expérience les cristaux grossisent en faisant des genre d'arbres. En revanche, sur la simulation, les cristaux augmentes en paté.

Afin de se rapprocher de la réalité, il semble important de changer la coupe faite. Il faudrait aussi prendre en compte l'air. En effet, sur l'expérience, l'air vient clairrement attirer le cristallisation changeant sa dynamique.

## Deuxième version, prise en compte de l'air

### Objectif et méthodes

A la suite du code précédent, on s'est rendue compte que pour avoir une forme plus proche de la réalité, il fallait prendre en compte la présence de l'air. Pour cela, on rajoute deux choses à la version précédente : 
- Si une case est proche d'un cristal et d'une case d'air, on augmente la probabilité de cristallisation (en augmentant artifficiellement le nombre de voisin).

- A chaque nouveau cristau, on s'assure que l'eau remonte d'un cran (pas de modèle de capilarité).

### Résultats

![](Modèle_2_creeping.png)

### Discussion

On observe que l'on est déjà plus proche de l'expérience. On voit le point de départ de la cristallisation et la diffusion assez clairement. Cependant cela est loin d'être parfait. Les cristaux n'on pas encore la bonne forme, on a pas d'échelle (ni pour le pas de temps ni pour le pas d'espace)...

De plus, les critères précédent sont très arbitraires pour caractériser la ressemblance à la réalité. Ils semblent donc qu'il y ait maintenant deux pistes à suivre : 

- Trouver des modèles physiques pour les différentes probabilités afin d'obtenir un modèle plus cohérent. Cela devrait dans le même temps donner les échelles à avoir pour la modélisation.

- Trouver des critères plus objectifs pour s'assurer de la ressemblance du milieu (simension fractal pour caractériser la porosité...).

## Le modèle physique
### Explication du modèle pour les probabilités
On essaie un premier modèle physique assez simple. On essaie d'estimer la différence d'énergie entre avant la cristallisation et après. Pour cela on sépare cette différence en deux :

- La première correspond à la différence entre les ions dans l'eau et sous forme de cristal. Cette première contribution volumique est commune à toutes les probabilités et sera donc supprimer au final dans la normalisation. On ne la prends donc pas en compte. 
- La deuxième contribution correspond aux liaisons entre le nouveau cristal et celui déjà existant. Ce cas va dépendre du nombre de bord commun. On estime ce terme à E=nb liaison * énergie d'une liaison. 

On pose l = longueur d'une liaison, dx le pas de la simulation, e l'épaisseur de cristal et E_l l'énergie de liaison et n le nb de bord commun avec un ancien cristal. On arrive avec ce modèle à : 

![](dev_theorique_proba.jpg)

Dans le programme, cela donne exp(A/dx). 

### Modèle pour la dynamique

![](dev_theorique_tps.jpg)

### Ajustements informatiques

Changement des règles de nucléations. Les nouveaux cristaux peuvent maintenant se former que en "parallèle" des anciens et plus dans les angles comme avant. 

### Résultats

![](Modèle_phys_creeping.png)

Les échelles sont en dixième de micromètres sur la simulation. Il y a eu 10 000 pas de temps.
 
L'image de l'expérience fait environ 100µm de large.

![](PICT0008.JPG)

On en déduit que les cristaux de la simulation sont encore trop petit. Plus de la taille de ceux coincé dans les interstice. Peut être liée au fait que l'on ne regarde pas la recombination des différents cristaux. Ce sera donc la prochaine étape.

## Analyse plus complète
Je modifie le code pour que nbCristaux non seulement énumère les cristaux mais vient également donner leur taille individuel. Cela permet d'avoir aisément accès à la distribution en taille des cristaux (en orange sur la courbe).

Avec une estimation grossière sur une vingtaine de cristaux, je crée une distribution expérimentale de la taille des cristaux (en bleu sur la courbe).

![](distribution_taille_cristaux.png)
(absisce en m^2 pas en m)

On observe que les cristaux sont un ordre de grandeur trop petit sur la modélisation. De plus, la distribution est exponentielle ce qui ne semble pas être le cas pour la réalité... 

Plusieur piste pour améliorer le code : 

- Prendre en compte les cristaux qui se colle ensemble.
- Enlever la dépendance au paramètres informatiques afin de pouvoir réduire la pas d'espace.

Les deux semblent compliquer à mettre en place sans repenser tous le code. Il serait donc bon de s'assurer que ce n'est pas partir dans la mauvaise direction;