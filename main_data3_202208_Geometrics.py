# -*- coding: utf-8 -*-
"""
Skrypt do wizualizacji wyników z Geometrics'a w odróżnieniu od drugiego skryptu do wizualizacji danych z Sensysa różni się tym, że w Sensycie mamy składowe X,Y,Z a tutaj tylko mamy Moduł

@author: Marcin
"""

import pandas as pd
import matplotlib.pyplot as plt

"""
UWAGA:
    Opis kluczy kaliber_(kierunek geograficzny skanowania)_(kat ułożenia rury względem kierunku jazdy)_(czy centralnie nad rura czy z boku)
    _C - pomiar nad obiektem
    _1W - pomiar na zachód o 1m
"""

#Słownik mapujący typ symulacji na pliki które użyto do danej symulacji.
#Uwag dla ułatwienia wszystkie wyniki są wgrane do jednego katalogu

fNames = {"75_NS_0_C":            ["Data_220801123850_0000", "Data_220801124007_0000", "Data_220801124450_0000"],
          "75_NS_90_C":           ["Data_220801125147_0000","Data_220801125432_0000","Data_220801125539_0000"],
          "75_NS_45_C":           ["Data_220801130520_0000","Data_220801130647_0000","Data_220801130812_0000"],
          "75_NS_pion_C":         ["Data_220801131716_0000","Data_220801131909_0000","Data_220801132033_0000"],
          "blacha_mala_0_C":           ["Data_220801134624_0000","Data_220801134729_0000","Data_220801134911_0000"],
          "blacha_mala_45_C":          ["Data_220801135307_0000","Data_220801135422_0000","Data_220801135543_0000"],
          "blacha_mala_pion_wzdłuz_C": ["Data_220801140841_0000","Data_220801140955_0000","Data_220801141122_0000"],
          "blacha_mala_pion_poprzek_C":["Data_220801142757_0000","Data_220801142938_0000","Data_220801143116_0000"],
          "tło_C":                ["Data_220801153017_0000","Data_220801153130_0000","Data_220801153234_0000"],
          "108_NS_0_C":           ["Data_220801144302_0000"
                                    "Data_220801144538_0000", # przedłużony start
                                    "Data_220801144730_0000"],
          "108_NS_45_C":          ["Data_220801145604_0000","Data_220801145739_0000","Data_220801145850_0000"],
          "108_NS_90_C":          ["Data_220801150517_0000","Data_220801150650_0000","Data_220801150754_0000"],
          "108_NS_pionowo_C":     ["Data_220801151805_0000","Data_220801151916_0000","Data_220801152010_0000"],
          "blacha_duza_pion_poprzech_C":["Data_220801153959_0000","Data_220801154306_0000","Data_220801154410_0000"],
          "blacha_duza_pion_wzdluz_C":["Data_220801154931_0000","Data_220801155056_0000","Data_220801155159_0000"],
          "blacha_duza_NS_0_C":["Data_220801155447_0000","Data_220801155551_0000","Data_220801155704_0000"],
          "blacha_duza_NS_45_C":["Data_220801155907_0000","Data_220801160018_0000","Data_220801160338_0000"],

 #Elementy przesunięte w bok o 1m
          "tło_1W" : ["Data_220803103245_0000",
                        "Data_220803103417_0000",
                        "Data_220803103513_0000"],
          "108_NS_0_1W" : ["Data_220803103940_0000","Data_220803104038_0000","Data_220803104144_0000"],
          "108_NS_45_1W":["Data_220803104538_0000","Data_220803104711_0000","Data_220803104815_0000"],
          "108_NS_90_1W":["Data_220803105024_0000","Data_220803105225_0000","Data_220803105328_0000"],
          "108_NS_0_pionowo_1W":["Data_220803105923_0000","Data_220803110046_0000","Data_220803110224_0000"],
          "blacha_duza_NS_0_1W":["Data_220803110611_0000","Data_220803110743_0000","Data_220803110916_0000"],
          "blacha_duza_NS_45_1W":["Data_220803111116_0000","Data_220803111212_0000","Data_220803111314_0000"],
          "blacha_duza_pion_wzdluz_1W":["Data_220803111636_0000","Data_220803111731_0000","Data_220803111822_0000"],
        # Test1_blacha_duza_pionowo_45_stopni:Data_220803112346_0000",
                                            # "Data_220803112441_0000",
                                            # "Data_220803112533_0000"],
          "blacha_duza_pion_poprzech_1W":["Data_220803113020_0000","Data_220803113117_0000","Data_220803113219_0000"],

          "75_NS_0_1W" : ["Data_220803114306_0000","Data_220803114352_0000","Data_220803114442_0000"],
          "75_NS_45_1W" : ["Data_220803114644_0000","Data_220803114739_0000","Data_220803114837_0000"],
          "75_NS_90_1W" : ["Data_220803115113_0000","Data_220803115206_0000","Data_220803115254_0000"],
          "75_NS_0_pionowo_1W":["Data_220803115549_0000","Data_220803115643_0000","Data_220803115730_0000"],
###---Blacha mala---###
          "blacha_mala_NS_0_1W":["Data_220803120337_0000","Data_220803120428_0000","Data_220803120518_0000"],
          "blacha_mala_NS_45_1W":["Data_220803120744_0000","Data_220803120834_0000","Data_220803120929_0000"],
          "blacha_mala_pion_wzdluz_1W":["Data_220803121326_0000","Data_220803121434_0000","Data_220803121537_0000"],
          # Test1_blacha_mala_pionowo_45_stopni:Data_220803121948_0000",
          #                         "Data_220803122044_0000",
          #                         "Data_220803122532_0000",
          "blacha_mala_pion_poprzech_1W":["Data_220803122711_0000","Data_220803122814_0000","Data_220803122933_0000"],
        }

#Ścieżka do katalogu z plikami
fDir = "D:/Projects/DataMining/scripts/CI/2021 SR Robotics/Badania fizyczne/Data3 2022.08.01/Geometrics/all/"
#"D:/Projects/DataMining/scripts/CI/2021 SR Robotics/Badania fizyczne/Data 75mm/phy/done_csv/"
plt.figure(15)
plt.clf()

keys = ["75_NS_0_C","75_NS_0_1W"] #Lista symulacji którą chcemy wyswietlic
         #"blacha_mala_0","blacha_mala_pion_wzdłuz","blacha_mala_45"

for key in keys:
    for fName in fNames[key]: #Jeli chcemy wywietlić wszystkie pliki z wynikami. Linijka do zakomentowania jesli chcemy tylko jeden
       # fName = fNames[key][1] #Odkomentowac gdy chcemy wyswietlic tylko jeden plik z wynikami, a nie wszystkie trzy
        df = pd.read_csv(fDir + fName + ".csv",header=0,sep=",")
        q = (df.loc[:,"M1"] + df.loc[:,"M2"])/2
        plt.plot(q,marker="o",label=key)
        plt.legend()

plt.title("Geometrics")
plt.show()