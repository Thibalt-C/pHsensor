#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:42:27 2024

@author: Clathi
"""


# recherche, installation et import des librairies
from pH_functions import *
try :
    import importlib.util
    import subprocess
    packages=['pyserial', 'datetime' , 'time' , 'numpy', 'matplotlib', 'os']
    for package in packages:
        spec = importlib.util.find_spec(package)
        if spec is None :
            subprocess.check_call(["pip", "install", package])
except :
    print("/!\ Échec de la vérification des librairies installées. Il est possible qu'il y ait une erreur dans l'importation des fonctions.")
    pass


# paramètres par défaut
a , b = 0.0117525 , 2.3659485
time_inter , nb_inter = 0.1 , 100
br = 19200
portIN = ''
default = [a , b , portIN , br , time_inter , nb_inter]


def launch(default) :
    """
    Initialisation du script, en vérifiant les dépendances de l'environnement en cours d'utilisation et en chargeant les éventuels paramètres pré-enregistrés pour celui-ci.

    Parameters
    ----------
    default : list
        Ensemble des paramètres par défaut.

    Returns
    -------
    computer : string
        Identification de l'utilisateur.
    a : float
        Pente de régression linéaire entre pH et voltage mesuré.
    b : float
        Ordonnée à l'origine de régression linéaire entre pH et voltage mesuré.
    portIN : string
        Identifiant du port série sur lequel le script doit lire des données.
    br : int
        Flux de données en baud.
    time_inter : float
        Temps d'intervalle entre chaque prélèvement de valeur au sein d'une mesure.
    nb_inter : int
        Nombre de valeurs utilisées pour constituer une mesure.
    s : serial.tools.list_ports_common.ListPortInfo
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié.

    """
        
    print('\n\n')
    print("      ##")
    print("     #  # ")
    print("    #    # ")
    print("   #      # ")
    print("  #        #")
    print(" #          #")
    print("#   SAFE-M   #    Soutenir l'apprentissage et les formations sur l'eau à Madagascar")
    print(" #          #                       https://morpho.ipgp.fr/safe-m/                 ")
    print("  #        #")
    print("   #      #")
    print("    ######")
    print('\n\n')
    print('Bonjour ! Ce pH-mètre a été conçu dans le cadre du projet SAFE-M.')
    print('Pour la documentation, consultez T. CHARDON, C. PALMIERI (2024) : https://github.com/Thibalt-C/pHsensor')     
    
    print('\n\n////////////////INITIALISATION////////////////\n')
    
    computer = os.getenv('HOME')
    
    try :
        settings = np.loadtxt('memory.txt',dtype=str,delimiter=',',skiprows=1)
        setting = settings[settings[:,0]==computer] ## cas de mémoire à plusieurs lignes enregistrées
        setting = setting[0][1:]
        print(f'Chargement des paramètres enregistrés pour {computer}.')
    except :
        try :
            setting = settings[settings[0]==computer] ## cas particulier de mémoire à ue seule ligne
            setting = setting[0][1:]
            print(f'Chargement des paramètres enregistrés pour {computer}.')
        except :
            print("/!\ Erreur de lecture de la mémoire. Les paramètres d'usine seront utilisés.")
            setting = default
            pass

    a , b , portIN , br , time_inter , nb_inter = setting
    portIN , s = port_connexion(br,portIN)
    time_inter , nb_inter = float(time_inter) , int(float(nb_inter))
    
    return computer , a , b , portIN , br , time_inter , nb_inter , s


def main(a,b,portIN,s,br,nb_inter,time_inter) :
    """
    Menu principal de l'interface utilisateur, dans lequel sont imbriquées les fonctions correspondant à chaque action. 
    Réceptionne les paramètres chargés par la fonction 'launch' et renvoie les paramètres éventuellement modifiés à la sortie du menu (option quitter).

    Parameters
    ----------
    a : float
        Pente de régression linéaire entre pH et voltage mesuré.
    b : float
        Ordonnée à l'origine de régression linéaire entre pH et voltage mesuré.
    portIN : string
        Identifiant du port série sur lequel le script doit lire des données.
    s : serial.tools.list_ports_common.ListPortInfo
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié.
    br : int
        Flux de données en baud.
    nb_inter : int
        Nombre de valeurs utilisées pour constituer une mesure.
    time_inter : float
        Temps d'intervalle entre chaque prélèvement de valeur au sein d'une mesure.

    Returns
    -------
    a : float
        Pente de régression linéaire entre pH et voltage mesuré.
    b : float
        Ordonnée à l'origine de régression linéaire entre pH et voltage mesuré.
    portIN : string
        Identifiant du port série sur lequel le script doit lire des données.
    br : int
        Flux de données en baud.
    nb_inter : int
        Nombre de valeurs utilisées pour constituer une mesure.
    time_inter : float
        Temps d'intervalle entre chaque prélèvement de valeur au sein d'une mesure.
    s : serial.tools.list_ports_common.ListPortInfo
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié.

    """
    
    action = None
    while action != 'Q' and action != 'q' :
        
        print('\n\n////////////////ACCUEIL////////////////\n')
        print('Nouvelle mesure : N \nEtalonnage : E \nParamètres : P \nQuitter : Q')
        action = input('>>> ')
        
        if action == 'N' or action == 'n' :
            print('\n\n////////////////MESURE////////////////\n')
            measurement(a , b , nb_inter , time_inter , s)
            
        elif action == 'E' or action == 'e' :
            print('\n\n////////////////CALIBRATION////////////////\n')
            print(f'Coefficients actuels : a = {a} , b = {b} (pente et valeur minimale).')
            a , b = calibration(nb_inter , time_inter , s)
            
        elif action == 'P' or action == 'p' :
            print('\n\n////////////////PARAMÈTRES////////////////\n')
            print('\nParamètres configurés :')
            print(f'   Port de connexion : {portIN}.')
            print(f'   Baudrate : {br}.')
            print(f'   Temps de mesure : {nb_inter*time_inter} sec.')
            print(f'   Nombre de valeurs dans une mesure : {nb_inter}.\n')
            portIN , s , br , nb_inter , time_inter  = fn_settings(portIN , s , br, nb_inter , time_inter)
        
        elif action == 'Q' or action == 'q' :
            break
        
        else:
            print('/!\ Saisie invalide.')    
    
    return a , b , portIN , br , nb_inter , time_inter , s


def save_settings(setting,s) :
    """
    Enregistre les paramètres éventuellement modifiés pendant l'utilisation du programme et interrompt la connexion avec l'appareil.

    Parameters
    ----------
    setting : list
        ensemble des paramètres à enregistrer : computer , a , b , portIN , br , time_inter , nb_inter
    s : serial.tools.list_ports_common.ListPortInfo
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié.

    Returns
    -------
    None.

    """

    print('\n\n////////////////EXTINCTION////////////////\n')

    new_settings = str('\n'+setting[0]+','+str(setting[1])+','+str(setting[2])+','+setting[3]+','+str(setting[4])+','+str(setting[5])+','+str(setting[6])).strip(' ')
    try :
        with open("memory.txt", "r") as f :
            lines = f.readlines()
        with open("memory.txt", "w") as f :
            for line in lines:
                if line.strip("\n").split(',')[0] != computer :
                    f.write(line)
            f.write(new_settings)
            print('Paramètres enregistrés pour ',computer)   
    except :
        print("/!\ Erreur de lecture de la mémoire. Création d'une nouvelle mémoire.")
        np.savetxt('memory.txt',[new_settings],delimiter=',',fmt='%s',header='#computer,a,b,portIN,br,time_inter,nb_inter',comments='#/!\ Settings storage – Please do not modify\n')
    print('À bientôt !')
    try :
        s.close()
    except :
        pass
    
    return


# ÉXÉCUTION DU PROGRAMME
computer , a , b , portIN , br , time_inter , nb_inter , s = launch(default)
a , b , portIN , br , nb_inter , time_inter , s = main(a , b , portIN , s , br , nb_inter , time_inter)
setting = computer , a , b , portIN , br , time_inter , nb_inter
save_settings(setting,s)
