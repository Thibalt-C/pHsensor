#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:09:59 2024

@author: Clathi
"""

import serial
import serial.tools.list_ports
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os


def port_connexion(br , portIN) :
    """
    Établit la connexion au port série.

    Parameters
    ----------
    br : int
        Flux de données en baud.
    portIN : string
        Identifiant du port série sur lequel le script doit lire des données.

    Returns
    -------
    port : string
        Identifiant du port série sur lequel le script doit lire des données.
    s : serial.tools.list_ports_common.ListPortInfo / string
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié. En cas d'échec de connexion, 's' sera une chaîne de caractères "erreur".

    """

    if portIN == '' :
        ports = list(serial.tools.list_ports.comports())
    else :
        ports = [portIN]  
    i = 0 
    conn = False
    while conn == False :
        try :
            port = ports[i] 
            if portIN == '' and (port.manufacturer == 'Arduino (www.arduino.cc)' or port.serial_number == '85035323234351504260'):
                port = port.device
                port = (port).replace('cu','tty')
                s = serial.Serial(port=port, baudrate=br, timeout=5) 
                conn = True  
                print('Connexion établie avec le port', port)
            else :
                s = serial.Serial(port=port, baudrate=br, timeout=5)
                conn = True
                print('Connexion établie avec le port', port)
        except :
            i += 1
            if i >= len(ports) :
                print("/!\ Port de connexion non détecté. Merci de rétablir la connexion non établie : connexion au processeur dans les réglages avant utilisation.")
                s = 'error' 
                portIN = '' 
                conn = True
            pass     
    return port , s


def pH_sensor(nb_inter , time_inter , s) :
    """
    Mesure du voltage du pH-mètre et de la température.

    Parameters
    ----------
    nb_inter : int
        Nombre de valeurs utilisées pour constituer une mesure.
    time_inter : float
        Temps d'intervalle entre chaque prélèvement de valeur au sein d'une mesure (moyenne de ces valeurs pour obtenir une mesure).
    s : serial.tools.list_ports_common.ListPortInfo
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié.

    Returns
    -------
    list_pH : list
        valeurs de voltages liées au pH et utilisées pour une mesure.
    list_temperatures : list
        valeurs de températures utilisées pour une mesure.

    """
    
    try :
        s.close()
        s.open()
        time.sleep(1)
    except :
        pass

    list_temperatures ,list_pH = [] , []
    err = 0 
    progression , restant = '' , int(nb_inter)
    for i in range(nb_inter) :
        try :
            values = s.readline().decode()
            values = values.split(";")
            temperature = float(values[0])
            list_temperatures.append(temperature)
            pH = float(values[1])
            list_pH.append(pH)
            progression += '*'
        except :
            err += 1
            progression += '!'
        restant -= 1
        barre = progression + restant * ' '
                    
        print(f'\r[{barre}]',flush=True, end='')
        time.sleep(time_inter) ## Time interval
    print('\n',err,f'problème(s) de lecture sur {nb_inter} mesures.\n')
    if err == nb_inter : 
        print('/!\ Un problème systématique semble empêcher la mesure. Veuillez vérifier la connexion à l\'appareil dans les paramètres.')
    return list_pH , list_temperatures   


def measurement(a , b , nb_inter , time_inter, s) :
    """
    Mesure unique ou en série et enregistrement éventuel des données.

    Parameters
    ----------
    a : float
        Pente de régression linéaire entre pH et voltage mesuré.
    b : float
        Ordonnée à l'origine de régression linéaire entre pH et voltage mesuré.
    nb_inter : int
        Nombre de valeurs utilisées pour constituer une mesure.
    time_inter : float
        Temps d'intervalle entre chaque prélèvement de valeur au sein d'une mesure.
    s : serial.tools.list_ports_common.ListPortInfo
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié.

    Returns
    -------
    None.

    """
    
    print('Voulez-vous enregistrer les données (format csv) ? (y/n)')
    data_rec = input('>>> ')
    valid = False
    while valid == False :
        try :
            nb_mesure = int(input("Nombre de mesures à effectuer : "))
            valid = True
        except :
            print('/!\ Saisie invalide, veuillez saisir un nombre entier.')  
    if nb_mesure != 1 :
        valid = False
        while valid == False :
            try :
                time_mesure = float(input("Intervalle de temps entre deux mesures (en sec) : "))
            except :
                time_mesure = -9999
                pass
            if time_mesure-time_inter*nb_inter >= 0:
                valid = True
            else:
                print(f"/!\ L'intervalle doit être supérieur ou égal à {time_inter*nb_inter} sec.")  
    LIST_DATES = []
    LIST_TEMP , LIST_TEMPSTD = [] , []
    LIST_PH , LIST_PHSTD = [] , []
    for mesure in range(nb_mesure) :     
        LIST_DATES.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        list_pH , list_temperatures = pH_sensor(nb_inter,time_inter,s)
        list_pH = np.array(list_pH)
        a , b = float(a) , float(b)
        list_pH = a*list_pH + b
        pH , pHstd = np.mean(list_pH) , np.std(list_pH)
        temp , tempstd = np.mean(list_temperatures) , np.std(list_temperatures)
        temp , tempstd = np.round(temp,2) , np.round(tempstd,4)
        pH , pHstd = np.round(pH,2) , np.round(pHstd,4)
        LIST_TEMP.append(temp)
        LIST_TEMPSTD.append(tempstd)
        LIST_PH.append(pH)
        LIST_PHSTD.append(pHstd)
        print(f'mesure nº{mesure+1}/{nb_mesure},',LIST_DATES[-1])
        print(f'   Température : {temp} °C \n   pH moyen : {pH} (écart-type : {pHstd})\n')
        if nb_mesure != 1 :
            time.sleep(time_mesure-time_inter*nb_inter)
    data = np.array([LIST_DATES , LIST_PH , LIST_PHSTD , LIST_TEMP , LIST_TEMPSTD]).T
    if data_rec == 'y' or data_rec == 'Y' :
        np.savetxt('mesure_pH_' + datetime.now().strftime("%m-%d-%Y_%Hh%Mm%Ss") 
                   + '.csv', data, delimiter=',', fmt='%s',
                   header= 'Date de mesure,pH,écart-type pH,Température,écart-type température')
    return 


def fn_settings(portIN , s , br , nb_inter , time_inter) :
    """
    Configuration des paramètres modifiables par l'utilisateur.

    Parameters
    ----------
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

    """
    
    print("Configurer le port de connexion : P \nChanger le flux (baudrate) : B \nChanger le temps et la fréquence de mesure : T")
    setting = input('>>> ')
    if setting == 'P' or setting == 'p':
        print('Saisissez le chemin du port (pour tester toutes les connexions périphériques de l\'ordinateur, laissez le champ vide)')
        port_name = input('>>> ')
        try :
            portIN , s = port_connexion(br, port_name)
        except Exception as inst :
            print("/!\ Echec de l'opération.")
            print('Erreur :',inst)
            pass
    elif setting == 'B' or setting == 'b' :
        try :
            br = int(input('Saisissez le nouveau baudrate : '))
            portIN , s = port_connexion(br, portIN)
            print('Paramètre enregistré.')
        except :
            print('/!\ Saisie invalide.')
            pass
    elif setting == 'T' or setting == 't' :
        try :
            time_measurement = float(input('Saisissez la durée d\'une mesure (sec) : '))
            nb_inter = int(input('Saisissez le nombres de valeurs composant une mesure : '))
            time_inter = time_measurement / nb_inter
            print("Une mesure comprend désormais ",nb_inter," valeurs, espacées entre elles de ",time_inter," secondes.\n")
        except :
            print('/!\ Saisie invalide.')
            pass
    else :
        print('/!\ Saisie invalide.')
    return portIN , s, br , nb_inter , time_inter


def calibration(nb_inter , time_inter, s):
    """
    Étalonnage assisté du voltage en fonction du pH.

    Parameters
    ----------
    nb_inter : int
        Nombre de valeurs utilisées pour constituer une mesure.
    time_inter : float
        Temps d'intervalle entre chaque prélèvement de valeur au sein d'une mesure.
    s : serial.tools.list_ports_common.ListPortInfo
        Objet Serial sur lequel on peut appliquer des fonctions d'ouverture, de lecture et de fermeture du port série affilié.

    Returns
    -------
    a : float
        Pente de régression linéaire entre pH et voltage mesuré.
    b : float
        Ordonnée à l'origine de régression linéaire entre pH et voltage mesuré.

    """
    
    valid = False
    while valid == False :
        try :
            nb_samples = int(input("Nombre d'étalons : "))
            valid = True
        except :
            print('/!\ Saisie invalide, veuillez saisir un nombre.')
    X , Y = [] , []
    for sample in range(nb_samples) :
        valid = False
        while valid == False :
            try :
                y = float(input('pH du tampon numéro ' + str(sample+1) + '/'  + str(nb_samples)+ ' : '))
                valid = True
            except :
                print('/!\ Saisie invalide, veuillez saisir un nombre.')
        print('Mesure en cours, veuillez patientez ',time_inter*nb_inter,' secondes')
        values , temp = pH_sensor(nb_inter , time_inter, s)
        x = np.mean(values)
        temp = np.mean(temp)
        if y == 4 or y == 7 or y == 10:
            print('Voulez-vous ajuster le pH en fonction de la température ? (y/n)')
            answer = input('>>> ')
            if answer == 'y' or answer == 'Y' :
                y = pH_temp_adjust(y,temp)
        X.append(x)
        Y.append(y)
    a , b = np.polyfit(X, Y, 1)
    R = np.corrcoef(X,Y)
    print('Calibration faite, valeurs de a et b :')
    print(a , b)
    print('Coefficient de corrélation (R^2) : ' , R[0,1])
    try :
        plt.figure()
        plt.scatter(X,Y)
        x_axis = np.linspace(np.min(X),np.max(X),100)
        plt.plot(x_axis,a*x_axis+b,'--')
        plt.xlabel('Voltage (u.a.)')
        plt.ylabel('pH')
        plt.show()
    except :
        pass
    
    return a , b


def pH_temp_adjust(pH , temp) :
    """
    Ajustement du pH étalon en fonction de la température par interpolation linéaire.

    Parameters
    ----------
    pH : int
        pH de la solution étalon.
    temp : float
        température mesurée de la solution.

    Returns
    -------
    pH_adjusted : float
        pH interpolé en fonction de correspondances entre pH et températures connues.

    """
    
    ## tables of values | source : HANNA intruments, Buffer solutions | uncertainties : ± 0.01 pH @ 25°C
    TEMPERATURES = np.arange(0,100,5)
    pH_4  = np.array([4.01,4.00,4.00,4.00,4.00,4.01,4.02,4.03,4.04,4.05,4.06,4.08,4.09,4.11,4.12,4.14,4.16,4.17,4.19,4.20])
    pH_7  = np.array([7.13,7.10,7.07,7.05,7.03,7.01,7.00,6.99,6.98,6.98,6.98,6.98,6.98,6.99,6.99,7.00,7.01,7.02,7.03,7.04])
    pH_10 = np.array([10.32,10.25,10.18,10.12,10.06,10.01,9.96,9.92,9.88,9.85,9.82,9.79,9.77,9.76,9.75,9.74,9.74,9.74,9.75,9.76])  
    if pH == 4:
        pH_adjusted = np.interp(temp,TEMPERATURES,pH_4)
    elif pH == 7:
        pH_adjusted = np.interp(temp,TEMPERATURES,pH_7)
    elif pH == 10:
        pH_adjusted = np.interp(temp,TEMPERATURES,pH_10)
    
    return pH_adjusted


