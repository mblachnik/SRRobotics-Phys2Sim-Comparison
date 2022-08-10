# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:45:09 2022

@author: Marcin
"""

import pandas as pd
import re
import io
import numpy as np
import os
import logging
import json

def read_num_sim(fName : str, columnsFile :str = '../Model ML/data_V4/columns_csv_V4.csv'):
    #Wczytanie pliku z nazwami kolumn
    columnNames = pd.read_csv(columnsFile)

    idXYZ = columnNames.loc[:,'Wartosc'].apply(lambda x: x[0] in 'XYZ')
    num = columnNames.loc[idXYZ,'Wartosc'].apply(lambda x: float(x[2:]))
    tx = columnNames.loc[idXYZ,'Wartosc'].apply(lambda x: x[0])

    columnNames.loc[idXYZ,"Wartosc"] = tx
    columnNames.loc[idXYZ,"id"] = num

    #Utworzenie wielopoziomowego indeksu - po to aby można było czytać dane po pojeździe
    index = pd.MultiIndex.from_frame(columnNames)
    #Tworzymy dataframe
    df = pd.read_csv(fName, header=[0])


    df.columns = index

    return df

def read_phys_data(fDir : str, sample_dist = 0.1, maxValue = 6.8, window_size = 7):
    """
    Parameters
    ----------
    fName : str
        DESCRIPTION.
    sample_dist : TYPE, optional
        DESCRIPTION. Odległsc między próbkami. Zgodnie z tym co bylo w eksperymentach komputerowych to sample byly brane co 10cm. The default is 0.1.
    maxValue : TYPE, optional
        DESCRIPTION. Zakres odległości w jakim porusza się obiekt. Oznacza to że poruszamy się od 0 do 6.8mThe default is 6.8.
    window_size : Okno uśredniania, optional
        DESCRIPTION. The default is 7.
    liczbaPojazow : TYPE, optional
        DESCRIPTION. Liczba pojazdów w roju The default is 5.

    Returns
    -------
    None.

    """
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    dirs = [x for x in os.walk(fDir)][1:] #Pomijamy pierwszy element bo to .
    dfs = []
    labels = []
    for di,sdi,fis in dirs:
        fName = min([fi for fi in fis if fi.endswith('.uxo')],key=len) #Z dostępnych plików znajdź kończące się na .uxo i wybierz najkrótszy - iinne mają dopiski _x,_y,_z
        fName = fName.replace('.uxo', '')
        df = magnetometer_read(os.path.join(di,fName))
        df = format_dataframe(df,window_size, maxValue, sample_dist)
        label = read_label(os.path.join(di,"label.txt"))
        dfs.append(df)
        labels.append(label)

    df =pd.concat(dfs,axis=0)
    df.reset_index(inplace=True, drop=True)
    return df


def magnetometer_read(fName, subtractMin=False):
    """

    Read single data file containing recorded signal from magnetometer
    Parameters
    ----------
    fName : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    dfs = []
    #mapowanieNaKOlumnyRomka = {'x':'Y', 'y':'X', 'z':'Z'} #Uwaga w modelu mat. jest inna kolejnoć kolumn ta mapa służy odpowiedniej konwersji
    mapowanieNaKOlumnyRomka = {'x':'X', 'y':'Y', 'z':'Z'}
    for i, c in enumerate('xyz'):
        #Otwórz plik i wczytaj do pamięci
        with open(fName + "_" + c + ".uxo", 'r') as file:
            lines = file.readlines()
        # Pominięcie nieistotnych linii, rozpoznawanie linii po identyfikatorze [xxx], [070] -nazwy kolumn, [072] - wartości
        lines = [line for line in lines if line.startswith(('[070]','[072]'))]
        # Usunięcie identyfikator linii oraz sklejenie elementów linii do jednego długiego stringu w postaci csv
        lines = ''.join([re.sub('\[\d+\]', '', x) for x in lines])
        data = io.StringIO(lines) #Tutaj udejemy że mamy plik, choć są to dane zgromadzone w pamięi
        # Wczytanie danych z stringu jako dataframeu
        dfTmp = pd.read_csv(data, sep=';', decimal=",")
        #Zmiana wartości z 1,2,3  na Pojazd_1, Pojazd_2, ...
        dfTmp['X [m]'] = dfTmp['X [m]'].apply(lambda x: 'Pojazd_'+str(int(x)+1))
        dfTmp.set_index(['X [m]','Y [m]'], inplace=True)
        #Pozbycie się niepotrzebnych kolumn
        dfTmp = dfTmp['Value [nT]']
        #Usunięcie niepotrzebnych wierszy
        idx = dfTmp.index.duplicated()
        logger = logging.getLogger(__name__)
        logger.info(f"Found: {np.sum(idx)} duplicated items")
        dfTmp = dfTmp[~idx]
        #Przeformatowanie danych, tak że Pjazd_1, Pojazd_2 itd stają się nowymi kolumnami
        dfTmp = dfTmp.unstack(0)
        if subtractMin:
            dfTmp = dfTmp-dfTmp.min().min()
        #Stworzenie nowego indeksu zgodnego z danymi uczącymi
        dfTmp.columns = pd.MultiIndex.from_product([dfTmp.columns,[mapowanieNaKOlumnyRomka[c]]])
        dfs.append(dfTmp)



    #Sklejenie dataframeów bo dfs zawiera wszystkie składowe X,Y,Z jako osobne elementy listy
    df = pd.concat(dfs, axis=1, )
    df.reset_index(inplace=True) #Zamieniamy indeks na zwykłą kolumnę (uwaga, brak drop)
    #Zmieniamy nazwę kolumny zawierającej dystans na "D"
    df = df.rename(columns={'Y [m]':'D'})
    return df


def convert_2D_to_3D_column_names(df):
    """
    COnverts column names from
    ('Pojazd_1', 'X_0') => ('Pojazd_1', 'X',  '0'),
    ('Pojazd_1', 'Y_0') => ('Pojazd_1', 'Y',  '0'),
    ('Pojazd_1', 'Z_0')) => (Pojazd_1', 'Z',  '0')

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    miRef = df.columns
    mi = miRef.to_frame()
    mi.reset_index(drop=True, inplace=True)
    meta = mi[mi[0]=='Meta']
    mi = mi[mi[0]!='Meta']
    num = mi.loc[:,1].apply(lambda x: float(x[2:]))
    tx = mi.loc[:,1].apply(lambda x: x[0])
    mi.loc[:,1] = tx
    mi.loc[:,2] = num

    meta.loc[:,2]=""
    mi = pd.concat([mi,meta],axis=0)


    mi.rename({0:'Pojazd', 1:'Wartosc', 2:'id'},axis=1,inplace=True)
    mi1 = pd.MultiIndex.from_frame(mi)
    df.columns = mi1
    return df

def format_dataframe(df:pd.DataFrame, window_size:int=7, maxValue:float=6.8, sample_dist:float = 0.1):
    """
    Process data from magnetometer.
    It includes:
        - moving window averagining in order to reduce the impact of noise
        - sampling the recorded magnetomater data with given period. Column D
          denotes the distances between samples

    Parameters
    ----------
    df : pandas.DataFrame
        input dataframe.
    window_size : int, optional
        The size of averaging window. The default is 7 (that is 7 samples)
    maxValue : float, optional
        The longest distance - this allows to limit the number of recorder samples when for different skannings - different objects once the distance was 7m and for the other 7.7m, and for some that is 6.5. The default is 6.8.
    sample_dist : float, optional
        The distance between the following samples. The default is 0.1.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    #Filtracja szumu przez uśrednienie
    df = df.rolling(window_size).mean()
    #Ponieważ f próbkowania jest większa niż zakładana, przez sample_dist więc próbkujemy są który wiersz
    if maxValue == None: maxValue = df['D'].max() + sample_dist
    steps = [i for i in np.arange(0,maxValue, sample_dist)]
    ids = []
    for step in steps:
        idd = np.argmin(np.abs(df['D'] - step))
        ids.append(idd)
    df = df.iloc[ids,:]
    dfs = []
    #Tutaj DF składa się z kolumn (Pojazd_1,X),(Pojazd_2,X)...(Pojazd_1,Z),...,(Pojzd_5,X) a wiersze to kolejne wartoci w funkcji odległoci i liczby te zamieniamy na jeden długi wiersz
    for colName in df.columns.levels[0][1:]:
    #for i in range(1,liczbaPojazow+1):
    #    colName = 'Pojazd_'+str(i)
        dfTmp = df[colName] #Odczytujemy składowe dla kolejnych pojazdów, wówczas dfTmp ma trzy składowe X,Y,Z
        sh = dfTmp.shape
        values = np.reshape(dfTmp.values, (1, np.prod(sh))) #Zamieniamy pojedynczy pojazd na jeden wiersz

        shortNames = list(dfTmp.columns)
        colNames = []
        for j in range(sh[0]):
            colNames = colNames + [a + '_' + str(j) for a in shortNames]
        dfRen = pd.DataFrame(values,columns=pd.MultiIndex.from_product([[colName], colNames]))
        dfs.append(dfRen)
    df = pd.concat(dfs, axis=1, )
    #Skalowanie z nanoTesli do Tesli
    df = df * 1e-9
    return df

def read_label(fName):
    with open(fName, 'r') as file:
        label = file.readline()
    return label


def addMetaToPhys(df, fMeta, rozmiarRury = [450, 800], wysokosci = [140, 240] ):
    """
    This function reads and adds metadata to the physical model.
    By default it reads meta data as provided by Sławek
    It recognizes wysokosc, długoć etc,

    Parameters
    ----------
    df : TYPE
        Input data which we want to extend with metadata
    fMeta : TYPE
        A json file which contains metadata

    Returns
    -------
    x : TYPE
        DataFrame identical to input data but with meta columns

    """
    def getMeta(metaData, dName):
        for x in metaData:
            if x["Katalog"] == dName:
                return x

    with open(fMeta) as f:
        metaFile = json.load(f)



    ress = list()
    for i in range(df.shape[0]):
        meta = getMeta(metaFile,df.loc[i,('Meta','DirName')].reset_index(drop=True)[0])
        res = {
         'fiy': 90 if meta["Orientacja"]=="WzdluzRuchu" else 0 if meta["Orientacja"]=="WPoprzekRuchu" else 45 if meta["Orientacja"]=="SkosRuchu" else 0,
         'fiz': 90 if meta["Orientacja"]=="Pion" else 0,
         'Wys': wysokosci[1] if meta["MagnetometryWysoko"] else wysokosci[0],
         'rura_dlugosc': rozmiarRury[1] if meta["DlugaRura"] else rozmiarRury[0],
         'Kat': 0 if meta["KierunkeEW"] else 90,
         'ref': not meta["JestObiekt"]}
        ress.append(res)

    df_meta = pd.DataFrame(ress)
    ml = [('Meta',x,'') for x in df_meta.columns]
    index = pd.MultiIndex.from_tuples(ml)
    df_meta.columns = index

    df = pd.concat([df, df_meta],axis=1)
    return df

def addBias(df,Be=40e-6,inklinacja = 67):
    """
    This funcion adds constant argument to each of coordinates of the magnetic field

    Parameters
    ----------
    df : TYPE
        The input dataframe with 3 level column index, where levels[1] contains coordinates X,Y,Z
    x : TYPE
        The value to be added to coordinate X
    y : TYPE
        The value to be added to coordinate Y
    z : TYPE
        The value to be added to coordinate Z

    Returns
    -------
    df : TYPE
        New dataframe with corrected values

    """
    inklinacja = np.radians(inklinacja)
    x = Be * np.cos(inklinacja)
    y = Be * np.sin(inklinacja)
    z = Be * 0
    df=df.copy()
    idx = df.columns.get_level_values(1)=='X'
    df.loc[:,idx] += x
    idy = df.columns.get_level_values(1)=='Y'
    df.loc[:,idy] -= y #- df.loc[:,idy]
    idz = df.columns.get_level_values(1)=='Z'
    df.loc[:,idz] += z
    return df

def subtractBacground(df,refs):
    """
    This function is used to subtracyt background from the recorded values. Here the refs is a dict in which
    keys  represent indexes of rows in df which contains the signals, and values represent indexes of recorded background signals,
    that are signals without the object.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    refs : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    cols = [ c for c in  df.columns if c[0] != 'Meta']
    colsMeta = [ c for c in  df.columns if c[0] == 'Meta']
    rows = list()
    for i,j in refs.items():
        row = df.loc[i,cols] - df.loc[j,cols]
        rowMeta = df.loc[i,colsMeta]
        row = pd.concat([rowMeta,row],axis=0)
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def fileNameParser(df, reffs):
    """
    Funkcja słuzy do parsowania nazw plików z wynikami symulacji np. nazwy plików z obliczeń romka mają zakodowane parametry obliczeń
    W celu parsowania podajemy dataframe i słownik o postaci:

        Struktura słownika:
           klucz - nazwa kolumny w której zostaną zapisane wyniki
           wartoć - tuple[0] numer kolumny po sparsowaniu nazwy pliku z której interesuje nas wartoć, zakładamy że wartoci w nazwie pliku oddzielone są _
                    tuple[1] funkcja używa do parsowania wartoci, np. gdy chcemy zrobić konwersję np. z str do int lub bardziej zaawansowaną konwersję
        np. reffs = {'rura_dlugosc':(2,lambda x :int(x))} dla nazwy pliku=real_mr_450_fiz0_fiy0
        Spowoduje że plik zostanie podzielony na ['real','nr','450','fiz0','fiy0'], a potem do drugiego elementu z listy zostanie zastosowana konwersja str->int


    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    reffs : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """

    for i,j in reffs.items():
        df.loc[:,('Meta',i,"")] = df.loc[:,('Meta','Nazwa')].iloc[:,0].str.split("_").apply(lambda x: x[j[0]]).apply(j[1])
    return df

    # reffs = {'rura_dlugosc':lambda x : int(x),
    #          'fiz':lambda x : int(x.replace("fiz","")),
    #          'fiy':lambda x : int(x.replace("fiy",""))}
    # for i,j in reffs.items():
    #     df.loc[:,('Meta',i,"")] = df.loc[:,('Meta',i,"")].apply(j)

def addModule(df):
    cols0 = df.columns.levels[0]
    cols0 = [col for col in cols0 if col!='Meta']
    dfs = list()
    dfs.append(df)
    for col in cols0:
        ndf = (df[col]['X']**2 + df[col]['Y']**2 + df[col]['Z']**2)**0.5
        nCols = [(col, 'M', idx) for idx in ndf.columns]
        mx = pd.MultiIndex.from_tuples(nCols)
        ndf.columns = mx
        dfs.append(ndf)
    df = pd.concat(dfs,axis=1)
    return df
