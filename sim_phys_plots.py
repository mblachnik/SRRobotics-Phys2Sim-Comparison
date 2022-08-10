import uxoProcessor as uxo
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

#Poniższe importy pozwalają na opcję Ctrl+C/Ctr;+V z obrazkami
#ADD copy-paste for figures
import matplotlib.font_manager as fm
from matplotlib.cm import get_cmap
import addcopyfighandler

def plotSkladowa(Xp,Xs,style='-',labels = ["Phy","Sim"]):
    Xp = Xp - (Xp[0]+Xp[-1])/2
    Xp.index = pd.Index([float(a) for a in Xp.index])
    mi = np.min(Xp.index)
    mx = np.max(Xp.index)
    dx = (mx-mi)/2
    Xp.index = pd.Index([a-dx for a in Xp.index])
    #Xp = Xp-np.mean(Xp)

    Xs.index = pd.Index([float(a) for a in Xs.index])
    mi = np.min(Xs.index)
    mx = np.max(Xs.index)
    dx = (mx-mi)/2
    Xs.index = pd.Index([a-dx for a in Xs.index])

    plt.plot(Xp,label=labels[0],linestyle=style)
    plt.plot(Xs,label=labels[1],linestyle=style)
    plt.legend()

def plotSkladowa2(df,style='-',label = "", centre=False):
    if centre:
        df = df  - (df[0]+df[-1])/2
    df.index = pd.Index([float(a) for a in df.index])
    mi = np.min(df.index)
    mx = np.max(df.index)
    dx = (mx-mi)/2
    df.index = pd.Index([a-dx for a in df.index])
    plt.plot(df,label=label,linestyle=style)

def plot1(df_phy,df_sim,id_phy,id_sim):
    """
    Identical to plot2 except eachfigure has unique axis

    Parameters
    ----------
    df_phy : TYPE
        DESCRIPTION.
    df_sim : TYPE
        DESCRIPTION.
    id_phy : TYPE
        DESCRIPTION.
    id_sim : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    Xp = df_phy.loc[id_phy,('Pojazd_3')]
    Xs = df_sim.loc[id_sim,('Pojazd_5')]

    skladowe = 'XYZM'
    for i,skladowa in enumerate(skladowe):
        plt.figure(i)
        plt.clf()
        plotSkladowa(Xp[skladowa], Xs[skladowa], style="-", labels=["Phy_3","Sim_5"])
        plt.title(skladowa)


    Xp = df_phy.loc[id_phy,('Pojazd_2')]
    Xs = df_sim.loc[id_sim,('Pojazd_4')]

    skladowe = 'XYZM'
    for i,skladowa in enumerate(skladowe):
        plt.figure(i)
        plotSkladowa(Xp[skladowa], Xs[skladowa],style=":", labels=["Phy_2","Sim_4"])
        plt.title(skladowa)


    Xp = df_phy.loc[id_phy,('Pojazd_4')]
    Xs = df_sim.loc[id_sim,('Pojazd_6')]

    skladowe = 'XYZM'
    for i,skladowa in enumerate(skladowe):
        plt.figure(i)
        plotSkladowa(Xp[skladowa], Xs[skladowa], style='-.', labels=["Phy_4","Sim_6"])
        plt.title(skladowa)



def plot2(df_phy,df_sim,id_phy,id_sim, skladowe_phy = 'XYZ', skladowe_sim = 'XYZ',
          pojazdy = [('Pojazd_3','Pojazd_5'),
                     ('Pojazd_4','Pojazd_6'),
                     ('Pojazd_2','Pojazd_4'),
                    # ('Pojazd_1','Pojazd_3'),
                    # ('Pojazd_5','Pojazd_7')
                    ]):
    """
    Creates a plot of recordet values.


    Parameters
    ----------
    df_phy : TYPE
        Input data with values recorded from phisical sensors
    df_sim : TYPE
        Input data with simulations
    id_phy : TYPE
        Id of row with phical data
    id_sim : TYPE
        Id of row with simulated data
    skladowe_phy : TYPE
        The order of coordinates to plot, it allows to replace standard order XYZM into another order when X is replaced by Z
    skladowe_sim : TYPE
       The order of coordinates to plot
    pojazdy : TYPE
        a list of typlea in form of (pojazd_id_phys,pojazd_id_sim), where the first element of a tuple is the name of Pojazd_id from physical model, and the second is the Pojazd_id from simulated data
    Returns
    -------
    None.

    """
    poj_phy = pojazdy[0][0]
    poj_sim = pojazdy[0][1]
    if df_phy is not None:
        Xp = df_phy.loc[id_phy,(poj_phy)]
    if df_sim is not None:
        Xs = df_sim.loc[id_sim,(poj_sim)]

 #Tutaj można podmienić
    axs = list()
    n = np.min((len(skladowe_phy),len(skladowe_sim)))
    for i in range(n):
        skladowaP = skladowe_phy[i]
        skladowaS = skladowe_sim[i]
        plt.figure(i)
        plt.clf()
        ax1 = plt.gca()
        if df_phy is not None:
            plotSkladowa2(Xp[skladowaP], style="-", label=poj_phy,centre=True)
            #plotSkladowa2(Xp[skladowaP], style="-", label=poj_phy)
            plt.legend(loc='upper left')
        ax2 =  ax1.twinx()
        axs.append((ax1,ax2))
        if df_sim is not None:
            plotSkladowa2(Xs[skladowaS], style=":", label=poj_sim)
            plt.legend(loc='upper right')
        plt.title(skladowaP + skladowaS)

    for id_pojazd in range(1,len(pojazdy)):
        poj_phy = pojazdy[id_pojazd][0]
        poj_sim = pojazdy[id_pojazd][1]
        if df_phy is not None:
            Xp = df_phy.loc[id_phy,(poj_phy)]
        if df_sim is not None:
            Xs = df_sim.loc[id_sim,(poj_sim)]

        for i in range(n):
           # plt.figure(i)
           skladowaS = skladowe_sim[i]
           skladowaP = skladowe_phy[i]
           plt.sca(axs[i][0])
           if df_phy is not None:
               plotSkladowa2(Xp[skladowaP], style="-", label=poj_phy,centre=True)
               #plotSkladowa2(Xp[skladowaP], style="-", label=poj_phy)
               plt.legend(loc='upper left')
           plt.sca(axs[i][1])
           if df_sim is not None:
               plotSkladowa2(Xs[skladowaS], style=":", label=poj_sim)
               plt.legend(loc='upper right')
           plt.title(skladowaP + skladowaS)
           #plt.title(skladowa)