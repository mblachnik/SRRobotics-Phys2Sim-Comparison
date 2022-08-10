# -*- coding: utf-8 -*-
"""
Analiza wpływu rotacji sensora dla Sensysa czyli wpływ zamontowania

Created on Mon Aug  1 13:02:19 2022

@author: Marcin
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Kluczo odpowiadaja tutaj rurze 108mm dla ktorej sensory w Geometrics'ie byly w roznych ulozeniach. Szczegoly, czym sie rozni A,A2 i B w opisie eksperymentow
fNames = {
          "108_A":           ["Test1_rura_fi_108_03_08_2022_13_09_25","Test2_rura_fi_108_03_08_2022_13_10_30","Test3_rura_fi_108_03_08_2022_13_11_36"], #Dane uszkodzone
          "108_A2":           ["Test_2_1_rura_fi_108_03_08_2022_13_30_06","Test_2_2_rura_fi_108_03_08_2022_13_31_01","Test_2_3_rura_fi_108_03_08_2022_13_32_15"],
          "108_B":          ["Test1_rura_fi_108_03_08_2022_13_17_40","Test2_rura_fi_108_03_08_2022_13_19_05","Test3_rura_fi_108_03_08_2022_13_23_23"],
        }


fDir = "D:/Projects/DataMining/scripts/CI/2021 SR Robotics/Badania fizyczne/Data3 2022.08/Sensys/Pomiary NS/rotacja sensysa/all/"
#"D:/Projects/DataMining/scripts/CI/2021 SR Robotics/Badania fizyczne/Data 75mm/phy/done_csv/"
plt.figure(1)
plt.clf()
keys = ["108_A2",
        "108_B"
        ]
#Czyscimy obrazki
for i,key in enumerate(keys):
    plt.figure(10+i)
    plt.clf()
    plt.figure(20+i)
    plt.clf()
    plt.figure(30+i)
    plt.clf()

plt.figure(4)
plt.clf()

#Rysujemy wykresy
for i,key in enumerate(keys):
    #for fName in fNames[key]:
        fName = fNames[key][2]
        df = pd.read_csv(fDir + fName + ".csv",header=0,sep=",")
        plt.figure(10+i)
        plt.plot(df.loc[:,"X"], label="X")
        plt.title("Sensys X")
        plt.figure(20+i)
        plt.plot(df.loc[:,"Y"], label="Y")
        plt.title("Sensys Y")
        plt.figure(30+i)
        plt.plot(df.loc[:,"Z"], label="Z")
        plt.title("Sensys Z")

        plt.figure(4)
        #Obliczamy modul
        m=np.sqrt(df.loc[:,"X"]**2 +df.loc[:,"Y"]**2+df.loc[:,"Z"]**2)
        plt.plot(m, label=key, marker="o")

        plt.title("Sensys M")

plt.legend()
plt.show()