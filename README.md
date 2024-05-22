# Conception d'un pH-mètre à bas-coût basé sur une puce Arduino

> Merci de citer ce travail de la façon suivante / Please refer to this work according to the following : ***T. CHARDON, C. PALMIERI (2024). Low cost pH sensor exploiting Arduino chip's capabilities. [User notice] Institut de Physique du Globe de Paris.***

Dans le cadre du projet SAFE-M (https://morpho.ipgp.fr/safe-m), les étudiantes et étudiants en licence à l'Institut de Physique du Globe de Paris ont eu pour mission de réaliser un appareil de mesure performant du pH et de la température. Cette conception a été réalisée sur la base de connaissances rudimentaires en électronique et C++, tout en s'appuyant sur des acquis en Python, qui constitue le script faisant office d'interface utilisateur.

## Composition

Le pH-mètre est équipé ainsi :
- Boîtier contenant l'électronique : carte Arduino Uno et connecteurs
- Port de connexion USB type C
- Sonde de mesure du pH et son capuchon rempli de solution neutre
- Sonde de mesure de la température

## Prérequis et compatibilité

Le pH-mètre en lui-même utilise le port série comme moyen de communication. Tout ordinateur disposant d'une connexion série remplit ainsi les prérequis.

En revanche, le script Python demande comme prérequis la présence d'un installateur de programmes pour Python 3 sur l'ordinateur (PyPI, Anaconda). La recherche du port de connexion a été optimisée pour les distributions Linux et pour MacOS et peut échouer sur Windows, il reste néanmoins toujours possible de configurer manuellement le port de connexion.

Ainsi, à peu près tout ordinateur disposant d'une invite de commandes (terminal) accessible à l'utilisateur pourra utiliser le pH-mètre via l'interface écrite en Python 3.

> /!\ La présence du module *serial* a été dans la phase de test du pH-mètre source d'erreurs dans l'éxécution du script. Il est nécessaire de désinstaller ce dernier et d'installer *pyserial*.

### Spécifications des appareils utilisés pour tester le pH-mètre

- MacBook Pro 2019, MacOS 14.4.1 (23E224), Python 3.10.12
- [ac] 


## Utilisation

Commencez par brancher le pH-mètre. Au branchement, le pH-mètre prendra une poignée de secondes avant d'émettre dans le port série sur lequel il pourra être identifié grâce à son numéro de série, son constructeur, etc.

### Initialisation

Le script peut être simplement éxécuté sur le terminal, dans le dossier où il est localisé, à l'aide de la commande :
``` Unix
python pH_main.py
```
Il est possible également d'utiliser la commande *python3*, ou encore de lancer le script sur un environnement de développement intégré (IDE) comme Spyder, PyCharm, etc.

Une fois lancé, le script va s'initialiser en passant par les étapes suivantes :
1. Vérification de la présence des modules Python requis
2. Installation des programmes manquants
3. Identification de l'ordinateur en cours d'utilisation
4. Import des paramètres précédents si enregistrés
5. Connexion au port précédemment enregistré ou recherche du port de connexion

L'ensemble de ces étapes peuvent être contournées si elles engendrent une erreur du programme, auquel cas des paramètres par défaut sont configurés, ou a minima des avertissements à l'utilisateur sont émis.

### Accueil

La page d'accueil propose quatre actions :
1. Effectuer une nouvelle mesure (N)
2. Calibrer le pH-mètre (C)
3. Changer les paramètres (P)
4. Quitter le programme et éteindre l'appareil (Q)

L'utilisateur peut sélectionner une action à faire en saisissant la lettre correspondant à celle-ci, en majuscule ou en minuscule. Une saisie ne correspondant pas à une action répertoriée renvoie une erreur, l'utilisateur est alors invité à effectuer une nouvelle saisie.

### Calibration

L'utilisateur est invité à choisir :
- Le nombre d'étalons (optimalement 3 ou plus)
- Le pH de chaque étalon
- (après la mesure pour calibration) Une option pour corriger par interpolation linéaire le pH en fonction de la température

> **Faire une calibration optimale :**
> - Il est nécessaire de commencer par l'étalon avec le pH le plus faible et de croître graduellement pour obtenir de meilleurs résultats.
> - Entre chaque mesure d'étalon, un temps d'adaptation du capteur à la solution (1-2 minutes) est à observer pour que la solution soit stabilisée.
> - Les étalons 4, 7 et 10 ont des tableaux de correspondance en fonction de leur température (données de Hanna Instruments : https://hannainst.com) qui permettent leur ajustement.


### Nouvelle mesure

L'utilisateur est invité à choisir :
- Le nombre de mesures à effectuer
- Le temps entre deux mesures (si plus d'une mesure)
- Si un fichier contenant les données doit être généré à la fin de la mesure

Le temps entre deux mesures doit être par définition supérieur au temps que prend une mesure à être réalisée. Le fichier créé contient les mesures de pH, de température (deux chiffres significatifs) et leurs écarts-types (quatre chiffres significatifs). 

### Paramètres

Il y a trois paramètres qui peuvent être modifiés :
- Flux d'information ou baudrate (B) : entre 19200 et 115200 bauds, au delà de cet intervalle il y a des risques de problèmes de lecture récurrents.
- Port de connexion (P) : permet de saisir un port manuellement ou de lancer une recherche du port série.
- Temps et fréquence de mesure (T) : la durée totale d'une mesure en secondes et le nombre de valeurs utilisées (et donc la fréquence d'itération au sein d'une mesure) ; les valeurs d'une mesure permettent de donner une moyenne et un écart-type de la mesure.

> /!\ Le baudrate est également défini dans le code Arduino. En cas de modification, il est nécessaire de le changer dans ce dernier et de téléverser le nouveau script Arduino sur le pH-mètre.

### Quitter et éteindre l'appareil


## Debug

### Téléversement du script Arduino

Le script Arduino est un code écrit en C++. Il fait office de consigne permanente donnée à la puce, qui a la capacité de lire les informations reçues par les capteurs et de les écrire sur le port série (ici le port de connnexion USB) afin que ces dernières soient accessibles sur l'appareil connecté.

Si la carte Arduino a été réinitialisée ou changée, il est nécessaire de lui téléverser de nouveau un script à faire éxécuter pour que celle-ci délivre les informations prévues.


### serial / pyserial
