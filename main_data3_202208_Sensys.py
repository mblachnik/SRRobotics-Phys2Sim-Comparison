# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 09:13:59 2022

@author: Marcin
"""

# -*- coding: utf-8 -*-
"""
Skrypt do wizualizacji wyników z Sensysa'a w odróżnieniu od drugiego skryptu do wizualizacji danych z Geometrics różni się tym, że w Sensycie mamy składowe X,Y,Z i obliczoną M a Geometricsie  mamy tylko Moduł

@author: Marcin
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#Katalog z danymi
fDir = "D:/Projects/DataMining/scripts/CI/2021 SR Robotics/Badania fizyczne/Data3 2022.08.01/Sensys/all/"
#"D:/Projects/DataMining/scripts/CI/2021 SR Robotics/Badania fizyczne/Data 75mm/phy/done_csv/"


#Słownik nazwa skanu - lista plików z danej symulacji
fNames = {"75_NS_0":["Test0_rura_fi_75_0_stopni_02_08_2022_13_01_09",
                     "Test1_rura_fi_75_0_stopni_02_08_2022_13_09_25",
                     "Test2_rura_fi_75_0_stopni_02_08_2022_13_10_12"],
          "75_NS_90":["Test1_rura_fi_75_90_sopni_02_08_2022_14_16_36",
                      "Test2_rura_fi_75_90_sopni_02_08_2022_14_17_48",
                      "Test3_rura_fi_75_90_sopni_02_08_2022_14_18_52"],
          "75_NS_45":["test1_rura_fi_75_45_stopni_02_08_2022_13_57_52",
                      "test2_rura_fi_75_45_stopni_02_08_2022_13_58_43",
                      "test3_rura_fi_75_45_stopni_02_08_2022_13_59_56"],
          "75_NS_pion": ["Test1_rura_fi_75_pionowo_02_08_2022_14_22_11_szarpanie",
                         "Test2_rura_fi_75_pionowo_02_08_2022_14_23_47",
                         "Test3_rura_fi_75_pionowo_02_08_2022_14_25_00",
                         "Test4_rura_fi_75_pionowo_02_08_2022_14_25_59"],
          "108_NS_0":["Test1_rura_fi_108_0_stopni_02_08_2022_15_02_53",
                     "Test2_rura_fi_108_0_stopni_02_08_2022_15_03_58",
                     "Test3_rura_fi_108_0_stopni_02_08_2022_15_04_58"],
          "108_NS_45":["Test1_rura_fi_108_45_stopni_02_08_2022_15_14_39",
                      "Test2_rura_fi_108_45_stopni_02_08_2022_15_15_34",
                      "Test3_rura_fi_108_45_stopni_02_08_2022_15_16_30"],
          "108_NS_90":["Test1_rura_fi_108_90_stopni_02_08_2022_15_08_00",
                      "Test2_rura_fi_108_90_stopni_02_08_2022_15_08_59",
                      "Test3_rura_fi_108_90_stopni_02_08_2022_15_10_00"],
          "108_NS_pion":["Test1_rura_fi_108_pionowo_02_08_2022_15_19_45",
                        "Test2_rura_fi_108_pionowo_02_08_2022_15_20_59",
                        "Test3_rura_fi_108_pionowo_02_08_2022_15_22_00"],
          "blacha_mala_0":           ["Test1_mala_blacha_0_stopni_02_08_2022_14_28_41",
                                      "Test2_mala_blacha_0_stopni_02_08_2022_14_30_09",
                                      "Test3_mala_blacha_0_stopni_02_08_2022_14_32_41"],
          "blacha_mala_45":          ["Test1_mala_blacha_45_stopni_02_08_2022_14_35_02",
                                      "Test2_mala_blacha_45_stopni_02_08_2022_14_36_02",
                                      "Test3_mala_blacha_45_stopni_02_08_2022_14_37_06"],
          "blacha_mala_pion_wzdłuz": ["Test1_mala_blacha_pionowo_wzdluz_02_08_2022_14_41_11",
                                      "Test2_mala_blacha_pionowo_wzdluz_02_08_2022_14_42_14",
                                      "Test3_mala_blacha_pionowo_wzdluz_02_08_2022_14_43_26"],
          "blacha_mala_pion_poprzek":["Test1_mala_blacha_pionowo_poprzech_02_08_2022_14_52_35",
                                      "Test2_mala_blacha_pionowo_poprzech_02_08_2022_14_53_53",
                                      "Test3_mala_blacha_pionowo_poprzech_02_08_2022_14_55_15"],
          "blacha_duza_pion_poprzech":["Test1_blacha_duza_pionowo_poprzech_02_08_2022_15_38_35",
                                       "Test2_blacha_duza_pionowo_poprzech_02_08_2022_15_39_43",
                                       "Test3_blacha_duza_pionowo_poprzech_02_08_2022_15_41_01"],
          "blacha_duza_pion_wzdluz":["Test1_blacha_duza_pionowo_wzdluz_02_08_2022_15_31_55",
                                     "Test2_blacha_duza_pionowo_wzdluz_02_08_2022_15_33_58",
                                     "Test3_blacha_duza_pionowo_wzdluz_02_08_2022_15_35_44"],
          "blacha_duza_NS_0":["Test1_blacha_duza_0_stopni_02_08_2022_15_24_39",
                              "Test2_blacha_duza_0_stopni_02_08_2022_15_25_35",
                              "Test3_blacha_duza_0_stopni_02_08_2022_15_26_25"],
          "blacha_duza_NS_45":["Test1_blacha_duza_45_stopni_02_08_2022_15_28_07",
                               "Test2_blacha_duza_45_stopni_02_08_2022_15_29_06",
                               "Test3_blacha_duza_45_stopni_02_08_2022_15_29_59"],
           }

#Listaa składowych które chcemy wywietlic. Można dac tylko plotTypes = 'M' to będziemy mieli tylko moduł
plotTypes = 'XYZM'

#Kazda ze skladowych rysowana jest na osobnym wykresie - tutaj je czyscimy
if "X" in plotTypes:
    plt.figure(1)
    plt.clf()
if "Y" in plotTypes:
    plt.figure(2)
    plt.clf()
if "Z" in plotTypes:
    plt.figure(3)
    plt.clf()
if "M" in plotTypes:
    plt.figure(4)
    plt.clf()

#Lista kluczy ktore chcemy wyswietlic
keys = ["blacha_mala_0", "blacha_duza_NS_0","75_NS_0","108_NS_0"]
for key in keys:
    #for fName in fNames[key]: #Jesli dla danego obiekty chcemy wyswietlic wszystkie 3 badania eksperymentalne to odkomentowac ta linie i akomentowac nastepna
        fName = fNames[key][1] #Jak chcemy wyswietlic tylko jeden skan dla danego typu skanu
        #Wczytanie pliku
        df = pd.read_csv(fDir + fName + ".csv",header=0,sep=",")
        #Wyswietlenie skanow
        if "X" in plotTypes:
            plt.figure(1)
            plt.plot(df.loc[:,"X"], label="X")
            plt.title("Sensys X")
        if "Y" in plotTypes:
            plt.figure(2)
            plt.plot(df.loc[:,"Y"], label="Y")
            plt.title("Sensys Y")
        if "Z" in plotTypes:
            plt.figure(3)
            plt.plot(df.loc[:,"Z"], label="Z")
            plt.title("Sensys Z")
        if"M" in plotTypes:
            plt.figure(4)
            m=np.sqrt(df.loc[:,"X"]**2 +df.loc[:,"Y"]**2+df.loc[:,"Z"]**2)
            plt.plot(m, label=key)
            plt.title("Sensys M")

plt.legend()
plt.show()