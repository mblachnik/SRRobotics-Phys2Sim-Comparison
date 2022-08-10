# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 19:09:06 2022

Skrypt służy do przetwarzania danych wygenerowanych przez skyrpt Sławka.
W tym dataframie kluczowa jest kolumna z nazwą pliku bo ona pozwala na odtworzenie
pozostałych metadanych w tym fz, fiy oraz długoć rury użytej w symulacjach które przygotował Romek
@author: Marcin
"""

import pandas as pd
import uxoProcessor as uxo
import matplotlib.pyplot as plt
import os

fName = "v5_wynik_n_real_pasma_05m.csv"
fName = 'v5_wynik_n__pasma_05m.csv'
dirName = "../Badania fizyczne/Data2 NumericalModel/"
dirName = '../Badania fizyczne/Data Plaskacz Duzy/'
dirName = '../Badania fizyczne/Data 75mm v2'
fNameRes = 'data_sim_75mm_v2.csv'

df = uxo.read_num_sim(os.path.join(dirName, fName))


reffs = {'rura_dlugosc':(2,lambda x :int(x)),
         'fiz':(3,lambda x :int(x.replace("fiz",""))),
         'fiy':(4,lambda x : int(x.replace("fiy","")))}
reffs = {"ulozenie_rury" : (0,lambda x :x)}
#Struktura mapy:
#   klucz - nazwa kolumny
#   wartoć - tuple[0] numer kolumny po sparsowaniu nazwy pliku z której interesuje nas wartoć, zakładamy że wartoci w nazwie pliku oddzielone są _
#            tuple[1] funkcja używa do parsowania wartoci, np. gdy chcemy zrobić konwersję np. z str do int lub bardziej zaawansowaną konwersję
#np. reffs = {'rura_dlugosc':(2,lambda x :int(x))} dla nazwy pliku=real_mr_450_fiz0_fiy0
#Spowoduje że plik zostanie podzielony na ['real','nr','450','fiz0','fiy0'], a potem do drugiego elementu z listy zostanie zastosowana konwersja str->int

df = uxo.fileNameParser(df, reffs)

df.to_csv(os.path.join('testData',fNameRes),    index=False)


# pId = 5
# plotId = 0
# p5X = df[('Pojazd_' + str(pId),'X')]
# p5Y = df[('Pojazd_' + str(pId),'Y')]
# p5Z = df[('Pojazd_' + str(pId),'Z')]
# plt.figure(1)
# plt.clf();
# plt.plot(p5X.loc[plotId,:], label ='X')
# plt.plot(p5Y.loc[plotId,:], label ='Y')
# plt.plot(p5Z.loc[plotId,:], label ='Z')
# plt.legend()



