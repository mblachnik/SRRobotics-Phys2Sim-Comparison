# -*- coding: utf-8 -*-
"""
Skrypt do porównania wyników symulacji z badaniami fizycznymi dla danych uzyskanych w 2021.06
Created on Tue May 10 17:09:52 2022

@author: Marcin
"""

import uxoProcessor as uxo
import pandas as pd
import os
import numpy as np



from sim_phys_plots import plotSkladowa, plotSkladowa2, plot1, plot2

fDir = '../Badania fizyczne/Data2 2022.06/Physical Model/komplet_poniedziaêek_25.06.21_SG_kompletInf/'
fMeta = os.path.join(fDir,'pomiary.json')

fSim = 'v5_wynik_n_real_pasma_05m.csv'
fSim = 'v5_wynik_n__pasma_05m.csv'
fDirSim = '../Badania fizyczne/Data2 NumericalModel/'

df = pd.read_csv(os.path.join('testData','data2_phys.csv'), header=[0,1,2])


df = uxo.addMetaToPhys(df, fMeta,wysokosci = [1.5, 2.4]) #Dodanie metadanych do modelu fizycznego (takie metadane są dostępne w modelu numerycznym)

#Słownik konwersji tj. któremu zestawowi wyników pomiarów odpowiada który plik z tłem
refs = {0:1,
        2:1,
        3:1,
        4:1,
        5:1,
        6:1,
        7:1,
        8:11,
        9:11,
        10:11,
        12:11,
        13:11,
        14:11,
        15:11}

#Usunięcie tła z modelu fizycznego
df_phy = uxo.subtractBacground(df, refs)
#df_phy = df

#Wyznaczenie modułów X,Y,Z dla danych z modelu fizycznego
df_phy = uxo.addModule(df_phy)

#Wczytanie danych symulacyjnych
df_sim = pd.read_csv(os.path.join('testData','data2_sim.csv'), header=[0,1,2])


#df_phy = uxo.addBias(df,Be=40e-6,inklinacja = 67) #These are the default values, but for simplicity when Be=0 there is now change
df_sim = uxo.addBias(df_sim,Be=0) #This line must be added befor caluclating module. Otherwise module will be incorectly calculated

#Dodanie modułu do modelu numerycznego
df_sim = uxo.addModule(df_sim)

#Pobranie metadanych
mp = df_phy['Meta']
ms = df_sim['Meta']

#Wskazanie nazwy pliku z modelem fizycznym który ma być analizowany

#nazwa_skanu = '20210621-120537_Export' #To jest obraz tła
nazwa_skanu = '20210621-120056_Export'
#nazwa_skanu = '20210621-131557_Export'
#nazwa_skanu = "20210621-121113_Export" #Krutka w poprzek
#nazwa_skanu = '20210621-122215_Export' #Długa w poprzek
#nazwa_skanu = '20210621-122621_Export' #długa, wzdłuż
#nazwa_skanu = '20210621-120056_Export' #krótka wzdłuż

#Identyfikacja wiersza w którym znajduje się wybrany plik z danymi
i = np.where(df_phy[('Meta','DirName','Unnamed: 1020_level_2')] == nazwa_skanu)[0][0]

#Poszukujemy pliku z symulacjami o podobnych właściwościach tj. na podstawie metadanych identyfikujemy równoważny rekord z modelu numerycznego
cols = ['fiz','fiy','rura_dlugosc','Kat','Wys']
id0 = np.ones(shape=[ms.shape[0],1],dtype=bool)
for col in cols:
    id1 = ms.loc[:,col].values==mp.loc[i,col].values
    print(col + " " + str(mp.loc[i,col].values))
    #print(id1.sum())
    id0 = np.logical_and(id0,id1)

ms1 = ms.loc[id0,:]
#Gdyby jakimś cudem znalazł się więcej niż jeden taki rekord to wyświetl komunikat lub gdyby odpowiedni zbiór wyników symulacyjnych nie istniał
if (ms1.shape[0]>1) | (ms1.shape[0]==0):
    print('Cos jest nie tak')
    exit()
j=ms1.index[0] #Odczytujemy index rekordu symulacyjnego

#plot1(df_phy,df_sim,i,j)

#Rysujemy porównanie obydwu rekordów
plot2(df_phy,df_sim,i,j)

