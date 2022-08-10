# -*- coding: utf-8 -*-
"""
Skrypt do analizy i wyswietlania danych z badań eksperymentalnych wykonanych 2022.08
Created on Tue May 10 17:09:52 2022

@author: Marcin
"""

import uxoProcessor as uxo
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np



# fDir = '../Badania fizyczne/Data2/komplet_poniedziaêek_25.06.21_SG_kompletInf/'
# fMeta = os.path.join(fDir,'pomiary.json')

#Nazwa pliku z danymi
fSim = 'data3_sim_75mm_v2.csv'
idSymulacji = 42 #Numer wiersza (indeks) który będzie wczytywany do symulacji
idPojazdu = "Pojazd_7"

df_sim = pd.read_csv(os.path.join('testData',fSim), header=[0,1,2])
#Dodanie składowej stałej
df_sim = uxo.addBias(df_sim,Be=40e-6) #This line must be added befor caluclating module. Otherwise module will be incorectly calculated
#Dodanie modułu
df_sim = uxo.addModule(df_sim)

plt.figure(2)
plt.clf()
#Pobranie wyników dla danego wiersza i dla danego pojazdu - tutaj odczytujemy tylko moduł
mod = df_sim.loc[idSymulacji,(idPojazdu,"M")]
plt.plot(mod)

#plt.legend()



