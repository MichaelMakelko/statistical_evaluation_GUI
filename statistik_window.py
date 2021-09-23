# importiere Bibliotheken
from tkinter import *
from tkinter import messagebox
import pandas as pd
from pandastable import Table
from tkcalendar import *
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt, matplotlib.font_manager as fm
import seaborn as sns

# def statistik_module():
#     test = open_statistik().optionStat
    
#     print(test)
#     number = str(optionStat.get()) # ausgewählte Visualisierungsmethode aus den Radiobuttons
#     print("ausgewäte nummer", number)

#     # standartabweichung  
#     if (number == "1"):
#         print("")
#     #median
#     elif (number == "2"):
#         print("")
#     #mittelwert
#     elif (number == "3"):
#         print("")
#     # maximum
#     elif (number == "4"):
#         from Stats import merged_df
#         print(merged_df)
#         # erstelle neuen aufbereitetes DataFrame welche den maximalen wert jedes tages finded
#         df_new = merged_df.loc[merged_df.groupby(pd.Grouper(freq="D")).max().iloc[:,0]]
#         print(df_new)
#     # minimum
#     elif (number == "4"):
#         print("")

# def enableStat():
#     StatistikBtn['state'] = tk.NORMAL


def maximum():
    # immer wenn eine Funktion angesprochen wird mit klammer () angesprochen wenn nichts übergeben wird / sonst unkorrekte ausgaben
    df = df_for_statistic()
    print("import df:")
    print(df)
    df_new = (df.groupby(pd.Grouper(key="longtime",freq="D"))
            .agg({df.columns[1]: np.max})
            .reset_index())
    print(df_new)
    df_new = pd.DataFrame(data= df_new)
    print(df_new)

    # Visualiesierung
    ####
    family = 'DejaVu Sans'
    label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
    title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
    ####
    ax = df_new.plot(x ="longtime", y=df_new.columns[1], kind="line" ,figsize=[15, 5], linewidth=0.5, alpha=0.8, color="#003399")
    ax.yaxis.grid(True)
    ax.set_xlabel("Datum", fontproperties = label_font)
    ax.set_title("Maximum-Werte / Liniendiagramm / Auflösung Tag", fontproperties=title_font)
    plt.show()


def minimum():
    # immer wenn eine Funktion angesprochen wird mit klammer () angesprochen wenn nichts übergeben wird / sonst unkorrekte ausgaben 
    df = df_for_statistic()
    df_new = (df.groupby(pd.Grouper(key="longtime",freq="D"))
            .agg({df.columns[1]: np.min})
            .reset_index())

    print(df_new)
    df_new = pd.DataFrame(data= df_new)

    # Visualiesierung
    ####
    family = 'DejaVu Sans'
    label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
    title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
    ####
    ax = df_new.plot(x ="longtime", y=df_new.columns[1], kind="line" ,figsize=[15, 5], linewidth=0.5, alpha=0.8, color="#003399")
    ax.yaxis.grid(True)
    ax.set_xlabel("Datum", fontproperties = label_font)
    ax.set_title("Minimum-Werte / Liniendiagramm / Auflösung: Tag", fontproperties=title_font)
    plt.show()
    
    
def mittelwert():
    # immer wenn eine Funktion angesprochen wird mit klammer () angesprochen wenn nichts übergeben wird / sonst unkorrekte ausgaben 
    df = df_for_statistic()
    df_new = (df.groupby(pd.Grouper(key="longtime",freq="D")).agg({df.columns[1]: np.mean}).reset_index())

    print(df_new)
    df_new = pd.DataFrame(data= df_new)

    # Visualiesierung
    ####
    family = 'DejaVu Sans'
    label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
    title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
    ####
    ax = df_new.plot(x ="longtime", y=df_new.columns[1], kind="line" ,figsize=[15, 5], linewidth=0.5, alpha=0.8, color="#003399")
    ax.yaxis.grid(True)
    ax.set_xlabel("Datum", fontproperties = label_font)
    ax.set_title("Mittelwerte / Liniendiagramm / Auflösung: Tag", fontproperties=title_font)
    plt.show()

def standartabweichung():
    # immer wenn eine Funktion angesprochen wird mit klammer () angesprochen wenn nichts übergeben wird / sonst unkorrekte ausgaben 
    df = df_for_statistic()
    df_new = (df.groupby(pd.Grouper(key="longtime",freq="D"))
            .agg({df.columns[1]: np.std})
            .reset_index())

    print(df_new)
    df_new = pd.DataFrame(data= df_new)

    # Visualiesierung
    ####
    family = 'DejaVu Sans'
    label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
    title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
    ####
    ax = df_new.plot(x ="longtime", y=df_new.columns[1], kind="line" ,figsize=[15, 5], linewidth=0.5, alpha=0.8, color="#003399")
    ax.yaxis.grid(True)
    ax.set_xlabel("Datum", fontproperties = label_font)
    ax.set_title("Standartabweichung / Liniendiagramm / Auflösung: Tag", fontproperties=title_font)
    plt.show()

def Median():
    # immer wenn eine Funktion angesprochen wird mit klammer () angesprochen wenn nichts übergeben wird / sonst unkorrekte ausgaben 
    df = df_for_statistic()
    df_new = (df.groupby(pd.Grouper(key="longtime",freq="D")).agg({df.columns[1]: np.median}).reset_index())

    print(df_new)
    df_new = pd.DataFrame(data= df_new)

    # Visualiesierung
    ####
    family = 'DejaVu Sans'
    label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
    title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
    ####
    ax = df_new.plot(x ="longtime", y=df_new.columns[1], kind="line" ,figsize=[15, 5], linewidth=0.5, alpha=0.8, color="#003399")
    ax.yaxis.grid(True)
    ax.set_xlabel("Datum", fontproperties = label_font)
    ax.set_title("Median-Werte / Liniendiagramm / Auflösung: Tag", fontproperties=title_font)
    plt.show()


# diese Funktion importiert den aktuellen zusammengelegten DataFrame
def df_for_statistic():
    from kalender_window import df_date
    from datensatz_window import df_gui
    merged_df = pd.merge(df_date, df_gui , left_index=True, right_index=True)
    print("jetzt in der import merged_df Funktion")
    print(merged_df)
    return merged_df
    

def boxStunden():
    from datensatz_window import axeTitle
    df = df_for_statistic()
    df["hour"] = df.longtime.dt.hour
    ax= sns.boxplot(data=df, x="hour", y=df.columns[1])
    ax.axes.set_title(f"{df.columns[1]}"+" Auflösung: Stunden")
    ax.set_ylabel(axeTitle)
    plt.show()

def boxTage():
    from datensatz_window import axeTitle
    df = df_for_statistic()
    df["day"] = df.longtime.dt.day
    ax = sns.boxplot(data=df, x="day", y=df.columns[1])
    ax.axes.set_title(f"{df.columns[1]}"+" Auflösung: Tage")
    ax.set_ylabel(axeTitle)
    plt.show()

def boxMonate():
    from datensatz_window import axeTitle
    df = df_for_statistic()

    df["month"] = df.longtime.dt.month
    ax = sns.boxplot(data=df, x="month", y=df.columns[1])
    ax.axes.set_title(f"{df.columns[1]}"+" Auflösung: Monate")
    ax.set_ylabel(axeTitle)
    plt.show()

# ergänzende Funktion für die Combobox1
def newselection(event):
    print('selected:', event.widget.get())
    compare = event.widget.get()
    
    if compare == "Standartabweichung":
        standartabweichung()
    if compare == "median":
        Median()
    if compare == "Mittelwert":
        mittelwert()
    if compare == "maximum":
        maximum()
    if compare == "minimum":
        minimum()


# ergänzende Funktion für die Combobox2
def newselection2(event):
    messagebox.showinfo("Information", "Bitte gehen Sie sicher, dass Sie entsprechend der Auflösung auch den Zeitraum ebenso eingetsellt haben! Eine andere auswahl z.B. von Tage auf Stunden ist er möglich wenn 1.zurückgesetzt wurde 2. der Zeitraum angepasst wurde.")
    print('selected:', event.widget.get())
    compare = event.widget.get()
    
    if compare == "Stunden":
        boxStunden()
    if compare == "Tage":
        boxTage()
    if compare == "Monate":
        boxMonate()
        


def open_statistik():

    statistik = Tk()
    statistik.title("statistisches Verfahren wählen")
    #---------------------------------------------------------------------------------------------#
    frame_statistik = ttk.LabelFrame(statistik, text="statistische Verfahren")
    frame_statistik.pack(side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    # COMBOBOX STATISTISCHE VERFAHREN
    fr = ttk.Frame(frame_statistik)
    fr.pack(side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#

    cb1_label = ttk.Label(fr, text= "Anwendung auf Liniendiagramm" )
    cb1_label.grid(column=0, row=0, padx=5, pady=5)

    cb1 = ttk.Combobox(fr, values=('Standartabweichung', 'median', 'Mittelwert', 'maximum', 'minimum'))
    cb1.grid(column=0, row=1, padx=5, pady=5)
    cb1.bind("<<ComboboxSelected>>", newselection)

    #---------------------------------------------------------------------------------------------#
    frame_statistik = ttk.LabelFrame(statistik, text="Boxplot Einstellungen")
    frame_statistik.pack(side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    # COMBOBOX AUFLÖSUNG BOXPLOT
    fr = ttk.Frame(frame_statistik)
    fr.pack(side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    cb2_label = ttk.Label(fr, text= "Boxplot Darstellungen" )
    cb2_label.grid(column=0, row=0, padx=5, pady=5)

    # folgend soll die Auflösung des Boxplot angezeigt werden können
    cb2 = ttk.Combobox(fr, values=('Stunden', 'Tage', 'Monate'))
    cb2.grid(column=0, row=1, padx=5, pady=5)
    cb2.bind("<<ComboboxSelected>>", newselection2)

    #---------------------------------------------------------------------------------------------#
    fr = ttk.Frame(frame_statistik)
    fr.pack(side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    KalButton = ttk.Button(fr, text="Beenden", command=statistik.destroy)
    KalButton.grid(column=1 , row=0 , padx=5, pady=5)

