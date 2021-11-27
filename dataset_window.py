# importiere Bibliotheken
from tkinter import *
from tkinter import messagebox
import pandas as pd
from pandastable import Table
from tkcalendar import *
import tkinter as tk
from tkinter import ttk

# importiere Module aus andere Dateien
from preperation_data import temp_time, humi_time

def quit(x):
    x.destroy()


# Funktion gibt die Nummer des Sensor aus dem String zurück
def get_string_number(stringChoosen):
    # der String muss mit Leerzeichen getrennt werden um die Nummer/Zahl aus dem string filtern zu können
    a = stringChoosen.replace("_", " ")
    # folgende Funktion dient zum filtern der Nummer des ausgewählten strings
    SensNumber = [int(s) for s in a.split() if s.isdigit()]
    for i in SensNumber:
        if i > 0:
            save_number_string = str(i)
            return save_number_string



# funktion wird aktiviert wenn Button OK gedrückt wird
def on_click_temp():
    # varibale muss global deklariert werden damit Sie in einer anderen Datei importiert werden kann
    global df_gui
    global stringChoosen
    global save_number
    global axeTitle
    # flagge um die Buttons im menu zu aktievieren
    global flag2
    flag2 = True

    # übergebe den Titel für die Y-Achse
    axeTitle = "Temperatur"
    # setzen des Hackens im Menü Fenster
    #CheckVarData.set(True)
    # bekomme das ausgewählte column aus dem OptionMmenu
    val_temp = selected_temp.get()
    stringChoosen = val_temp
    save_number = get_string_number(stringChoosen)
    #übergege den column in ein neue DataFrame
    df_gui = temp_time[f"{val_temp}"]
    df_gui = pd.DataFrame(data=df_gui)
    # entferne für die Anzeigetabelle die NaN-Werte
    df2_clear = df_gui.dropna()
    buttonhumi['state'] = tk.DISABLED
    show_tabel(df2_clear)

def on_cklick_humi():
    # varibale muss global deklariert werden damit Sie in einer anderen Datei importiert werden kann
    global df_gui
    global stringChoosen
    global save_number
    global axeTitle
    # flagge um die Buttons im menu zu aktievieren
    global flag2
    flag2 = True
    # übergebe den Titel für die Y-Achse
    axeTitle = "Luftfeuchtigkeit"
    # setzen des Hackens im Menü Fenster
    #CheckVarData.set(True)

    # abspeichern des ausgewählten Senbsors als string
    val_humi = selected_humi.get()
    stringChoosen = val_humi
    save_number = get_string_number(stringChoosen)
    df_gui = humi_time[f"{val_humi}"]
    df_gui = pd.DataFrame(data=df_gui)
    df_humi_clear = df_gui.dropna()
    buttontemp['state'] = tk.DISABLED
    show_tabel(df_humi_clear)


# es wird eine externe Funktion verwednet um DataFrames als Tabellen anzuzeigen
def show_tabel(table):
    global tabelleSens
    # neues Fenster erstellen um den ausgewählten Sensor anzuzeigen
    tabelleSens = Tk()
    tabelleSens.title("Tabelle - ausgewählter Sensor")
    #---------------------------------------------------------------------------------------------#
    frame_tabelle_sens = ttk.Frame(tabelleSens)
    frame_tabelle_sens.pack(fill=X, side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    pt = Table(frame_tabelle_sens, dataframe=table)
    pt.show()


# derklarieren des zurücksetzten Taste  
def refresh_datensatz_window():
    buttontemp['state'] = tk.NORMAL
    buttonhumi['state'] = tk.NORMAL
    # entfernen des Hackens im Menü Fenster
    #CheckVarData.set(False)
    # setze den Status zurück wenn Zurücksetzten betätigt wurde
    # Fenster des ausgewählten Zeitraums wird geschlossen
    quit(tabelleSens)




def open_datensatz():
    global selected_temp
    global selected_humi
    global buttonhumi
    global buttontemp

    datensatz = Tk()
    datensatz.title('Datensatz aus der Datenbank wählen')
    #---------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------#
    # erstellen einen conatiner für die Info Box
    über_Frame = ttk.Frame(datensatz)
    über_Frame.pack(side=LEFT, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------#
    fr = ttk.LabelFrame(über_Frame, text= "Datenbank Struktur")
    fr.pack(side=TOP)
    #---------------------------------------------------------------------------------------------#
   
    # Einstellungen treeview
    treeview = ttk.Treeview(fr)
    treeview.grid(padx=5, pady=5)

    # Eltern deklarieren
    treeview.insert("", "0", "item1", text="sa_makelko")
    # Kinder deklarieren
    treeview.insert("item1", "end", "item_Tables", text="Tables")
    treeview.insert("item1", "end", "item_Views3", text="Views")
    treeview.insert("item1", "end", "item_Stored Procedures", text="Stored Procedures")
    treeview.insert("item1", "end", "Functions", text="Functions")

    # Inserting more than one attribute of an item
    treeview.insert('item_Tables', 'end', 'Algorithm', text ='Algorithm') 
    treeview.insert('item_Tables', 'end', 'Data structure', text ='Data structure')
    treeview.insert('item_Tables', 'end', '2018 paper', text ='2018 paper') 
    treeview.insert('item_Tables', 'end', '2019 paper', text ='2019 paper')



    #---------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------#
    # erstellen einen conatiner für die Info Box
    über_Frame = ttk.Frame(datensatz)
    über_Frame.pack(side=LEFT, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------------------#
    fr = ttk.LabelFrame(über_Frame, text= "aufbereiteter Datensatz")
    fr.pack(side=TOP)
    #---------------------------------------------------------------------------------------------#
    # Auswählen eines columns
    # bekomme die column Namen aus dem DataFrame
    values_temp = list(temp_time) 
    selected_temp = StringVar()
    # erstelln des Infotextes
    info_optionmenu = ttk.Label(fr, text="Temperatur-\ndaten wählen")
    info_optionmenu.grid(column=0, row=0, padx=5, pady=5)
    # erstelle einen Button der aufrollt und alle column namen anzeigt die ausgewählt werden können
    options = ttk.OptionMenu(fr, selected_temp, *values_temp)
    options.grid(column=0, row=1, padx=5, pady=5)
    # Button zum auswählen des columns
    buttontemp = ttk.Button(fr, text='Bestätigen', command=on_click_temp, state=tk.NORMAL)
    buttontemp.grid(column=1, row=0, padx=5, pady=5)


    values_humi = list(humi_time) 
    selected_humi = StringVar()
    # erstelln des Infotextes
    info_optionmenu_h = ttk.Label(fr, text="Luftfeuchtigkeits-\ndaten wählen")
    info_optionmenu_h.grid(column=0, row=3, padx=5, pady=5)
    # erstelle einen Button der aufrollt und alle column namen anzeigt die ausgewählt werden können
    options = ttk.OptionMenu(fr, selected_humi, *values_humi)
    options.grid(column=0, row=4, padx=5, pady=5)
    # Button zum auswählen des columns
    buttonhumi = ttk.Button(fr, text='Bestätigen', command=on_cklick_humi, state=tk.NORMAL)
    buttonhumi.grid(column=1, row=3, padx=5, pady=5)
    #---------------------------------------------------------------------------------------------#
    fr = ttk.LabelFrame(über_Frame, text= "Kommandos")
    fr.pack(side=TOP)
    #---------------------------------------------------------------------------------------------#
    
    zuButton = ttk.Button(fr, text="Zurücksetzen", command=refresh_datensatz_window)
    zuButton.grid(column=0 , row=0 , padx=5, pady=5)
    
    KalButton = ttk.Button(fr, text="Beenden", command=datensatz.destroy)
    KalButton.grid(column=1 , row=0 , padx=5, pady=5)