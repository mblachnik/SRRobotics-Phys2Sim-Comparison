# This script reads data recorded in 2021.06 which were stored in specific Sensys formet and coverts it into a file where each row represents datasample for machine learning - identical format to the one used for simulations
#Since 2022.08 SRRobotics has their owen file convertion script
import pandas as pd
import re
import io
import numpy as np
import os
import logging
import time
import matplotlib.pyplot as plt
import uxoProcessor as uxo

liczbaPojazow = 5 #Liczba pojazdów w roju
window_size = 7 #Okno uśredniania
maxValue = 6.8 #Zakres odległości w jakim porusza się obiekt. Oznacza to że poruszamy się od 0 do 6.8m
sample_dist = 0.1 #Odległsc między próbkami. Zgodnie z tym co bylo w eksperymentach komputerowych to sample byly brane co 10cm
fName = 'L1_ToraB-T0_Export'
fDir = '../Badania fizyczne/Data2 2022.06/Physical Model/komplet_poniedziaêek_25.06.21_SG_kompletInf/'


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dirs = [x for x in os.walk(fDir)][1:] #Pomijamy pierwszy element bo to
dfs = []
labels = []
for di,sdi,fis in dirs:
    fName = min([fi for fi in fis if fi.endswith('.uxo')],key=len) #Z dostępnych plików znajdź kończące się na .uxo i wybierz najkrótszy - iinne mają dopiski _x,_y,_z
    fName = fName.replace('.uxo', '')
    df = uxo.magnetometer_read(os.path.join(di,fName))
    df = uxo.format_dataframe(df,window_size, maxValue, sample_dist)
    dName = di[di.rfind('/')+1:]
    df.loc[0,('Meta','DirName')] = dName
    label = uxo.read_label(os.path.join(di,"label.txt"))
    dfs.append(df)
    labels.append(label)

df =pd.concat(dfs,axis=0)
df.reset_index(drop=True,inplace=True)
df = uxo.convert_2D_to_3D_column_names(df)

df.to_csv(os.path.join('testData','data_phys_1.csv'),index=False)
# dfLab = pd.DataFrame(labels,columns=['Labels'])
# dfLab.to_csv(os.path.join('testData','labels_1.csv'))
pass
