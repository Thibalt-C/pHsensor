# Conception d'un pH-mètre à bas-coût basé sur une puce Arduino

> Merci de citer ce travail de la façon suivante / Please refer to this work according to the following : ***T. CHARDON, C. PALMIERI (2024). Low cost pH sensor exploiting Arduino chip's capabilities. [User notice] Institut de Physique du Globe de Paris.***

Dans le cadre du projet SAFE-M (https://morpho.ipgp.fr/safe-m), les étudiantes et étudiants en licence à l'Institut de Physique du Globe de Paris ont eu pour mission de réaliser un appareil de mesure performant du pH et de la température. Cette conception a été réalisée sur la base de connaissances rudimentaires en électronique et C++, tout en s'appuyant sur des acquis en Python, qui constitue le script faisant office d'interface utilisateur.

## Composition

Le pH-mètre est équipé ainsi :
- Boîtier contenant l'électronique : carte Arduino Nano et connecteurs
- Port de connexion USB type C
- Sonde de mesure du pH et son capuchon rempli de solution neutre
- Sonde de mesure de la température

## Prérequis et compatibilité

Le pH-mètre en lui-même utilise le port série comme moyen de communication. Tout ordinateur disposant d'une connexion série remplit ainsi les prérequis.

En revanche, le script Python demande comme prérequis la présence d'un installateur de programmes pour Python 3 sur l'ordinateur (PyPI, Anaconda). La recherche du port de connexion a été optimisée pour les distributions Linux et pour MacOS et peut échouer sur Windows, il reste néanmoins toujours possible de configurer manuellement le port de connexion.

Ainsi, à peu près tout ordinateur disposant d'une invite de commandes (terminal) accessible à l'utilisateur pourra utiliser le pH-mètre via l'interface écrite en Python 3.

> /!\ La présence du module *serial* a été dans la phase de test du pH-mètre source d'erreurs dans l'éxécution du script. Il est nécessaire de désinstaller ce dernier et d'installer *pyserial*.

### Spécifications des appareils utilisés pour tester le pH-mètre


## Utilisation

Au branchement, le pH-mètre prendra une poignée de secondes avant d'émettre dans le port série sur lequel il pourra être identifié grâce à son numéro de série, son constructeur, etc.

### Initialisation

Le script peut être simplement éxécuté sur le terminal à l'aide de la commande :
> python /path/pH_sensor.py

Une fois lancé, le script va s'initialiser en passant par les étapes suivantes :
- Vérification de la présence des modules Python requis
- Installation des programmes manquants
- Identification de l'ordinateur en cours d'utilisation
- Import des paramètres précédents si enregistrés
- Connexion au port précédemment enregistré ou recherche du port de connexion

### Accueil

### Calibration

### Nouvelle mesure

### Paramètres

### Quitter et éteindre l'appareil


## Debug

### Téléversement du script Arduino

Le script Arduino est un code écrit en C++. Il fait office de consigne permanente donnée à la puce, qui a la capacité de lire les informations reçues par les capteurs et de les écrire sur le port série (ici le port de connnexion USB) afin que ces dernières soient accessibles sur l'appareil connecté.

Si la carte Arduino a été réinitialisée ou changée, il est nécessaire de lui téléverser de nouveau un script à faire éxécuter pour que celle-ci délivre les informations prévues.


### serial / pyserial
