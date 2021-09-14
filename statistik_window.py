# importiere Bibliotheken
from tkinter import *
from tkinter import messagebox
import pandas as pd
from pandastable import Table
from tkcalendar import *
import tkinter as tk
from tkinter import ttk
import numpy as np

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
    df_new = df.groupby(pd.Grouper(key="longtime",freq="D")).agg({df.columns[1]: [np.max]})
    print(df_new)


def minimum():
    # immer wenn eine Funktion angesprochen wird mit klammer () angesprochen wenn nichts übergeben wird / sonst unkorrekte ausgaben 
    df = df_for_statistic()
    print("import df:")
    print(df)
    
    


def df_for_statistic():
    from kalender_window import df_date
    from datensatz_window import df_gui
    merged_df = pd.merge(df_date, df_gui , left_index=True, right_index=True)
    print("jetzt in der import merged_df Funktion")
    print(merged_df)
    return merged_df
    



# folgende Funktion wählt das statistische Verfahren aus der combobox aus
def newselection(event):
    print('selected:', event.widget.get())
    compare = event.widget.get()
    
    if compare == "Standartabweichung":
        print("")
    if compare == "median":
        print("")
    if compare == "Mittelwert":
        print("")
    if compare == "maximum":
        print("gehe jetzt in die maximum funktion")
        maximum()
    if compare == "minimum":
        print("gehe in minimum")
        minimum()

def open_statistik():

    statistik = Tk()
    statistik.title("statistisches Verfahren wählen")
    #---------------------------------------------------------------------------------------------#
    frame_statistik = ttk.LabelFrame(statistik, text="statistische Verfahren")
    frame_statistik.pack(side=TOP,anchor=SW, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    fr = ttk.Frame(frame_statistik)
    fr.pack(side=TOP,anchor=SW, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    # StatistikBtn = ttk.Button(fr, text="Anwenden", command=statistik_module, state=tk.DISABLED)
    # StatistikBtn.grid(column=0, row=0, padx=5, pady=5)
    #---------------------------------------------------------------------------------------------#
    fr = ttk.Frame(frame_statistik)
    fr.pack(side=TOP,anchor=SW, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    # optionStat = IntVar()
    # r1 = ttk.Radiobutton(fr, text="standart-\nabweichung", variable=optionStat, value=1, command=enableStat)
    # r1.grid(column=0, row=0, padx=5, pady=5)
    # r2 = ttk.Radiobutton(fr, text="Median", variable=optionStat, value=2, command=enableStat)
    # r2.grid(column=1, row=0, padx=5, pady=5)
    # r3 = ttk.Radiobutton(fr, text="Mittel-\nwert", variable=optionStat, value=3, command=enableStat)
    # r3.grid(column=2, row=0, padx=5, pady=5)
    # r4 = ttk.Radiobutton(fr, text="oberes\nQuantil", variable=optionStat, value=4, command=enableStat)
    # r4.grid(column=3, row=0, padx=5, pady=5)
    # r5 = ttk.Radiobutton(fr, text="unteres\nQuantil", variable=optionStat, value=5, command=enableStat)
    # r5.grid(column=4, row=0, padx=5, pady=5)



    cb1 = ttk.Combobox(fr, values=('Standartabweichung', 'median', 'Mittelwert', 'maximum', 'minimum'))
    cb1.grid(column=0, row=1, padx=5, pady=5)
    cb1.bind("<<ComboboxSelected>>", newselection)

    cb2 = ttk.Combobox(fr, values=('X', 'Y', 'XX', 'XY'))
    cb2.grid(column=1, row=1, padx=5, pady=5)
    cb2.bind("<<ComboboxSelected>>", newselection)
