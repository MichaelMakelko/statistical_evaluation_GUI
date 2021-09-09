from tkinter import *
from prep_stats import temp_time, df_timestamp, choose_date_gui, commpare_date_input, firstLast_temp_df, firstLast_humi_df, first_string, last_string
from tkinter import messagebox
import pandas as pd
from pandastable import Table
from tkcalendar import *
import tkinter as tk
from tkinter import ttk




# erstes Datum für den Zeitruam wählen
def grab_date_first():
    global saveFirstDate
    global flag_A
    label_first_date.config(text=cal.get_date())
    # speicher das Datum ab
    saveFirstDate = cal.get_date()
    saveFirstDate = pd.to_datetime(saveFirstDate)

    fi = firstLast_temp_df["longtime"].iloc[0]
    la = firstLast_temp_df["longtime"].iloc[1]
    # prüfe ob das ausgewählte Datum in der Datenbank aufgenommen wurde
    if fi < saveFirstDate and la > saveFirstDate:
        pass
    else:
        ttk.messagebox.showwarning(title="Warnung", message="Das ausgewählte Datum ist nicht in der Datenbank aufgenommen")
    

# zweites Datum für den Zeitraum wählen
def grab_date_last():
    global saveLastDate
    global flag_B
    label_last_date.config(text=cal.get_date())
    # speicher das Datum ab
    saveLastDate = cal.get_date()
    # wandele das Datum von str in ein Timestamp um (für den vergelich notwendig)
    saveLastDate = pd.to_datetime(saveLastDate)

    fi = firstLast_temp_df["longtime"].iloc[0]
    la = firstLast_temp_df["longtime"].iloc[1]
    # prüfe ob das ausgewählte Datum in der Datenbank aufgenommen wurde
    if fi < saveLastDate and la > saveLastDate:
        pass
    else:
        ttk.messagebox.showwarning(title="Warnung", message="Das ausgewählte Datum ist nicht in der Datenbank aufgenommen")
    

# eingegebene Grenzen werden in ein DataFrame gefiltert
def df_filter_date():
    global tabelle
    global df_date
    df_date = choose_date_gui(saveFirstDate, saveLastDate)
    print(df_date)

    # neues Fenster erstellen um den ausgewählten Zeitraum anzuzeugen
    tabelle = Tk()
    tabelle.title("Tabelle - ausgewählter Zeitraum")
    #---------------------------------------------------------------------------------------------#
    frame_tabelle_date = ttk.Frame(tabelle)
    frame_tabelle_date.pack(fill=X, side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    pt = Table(frame_tabelle_date, dataframe=df_date)
    pt.show()


# derklarieren des zurücksetzten Taste  
def refresh_date_border_label():
    label_first_date.config(text="")
    label_last_date.config(text="")
    # Fenster des ausgewählten Zeitraums wird geschlossen
    quit(tabelle)


# folgende funktion schließt ein geöffnretes tkinter Fenster, ausgerufen aus einer funktion!
def quit(x):
    x.destroy()

# Kalender mittles .grid() positioniert
def open_kalender():
    global frame_tabelle_date
    global label_first_date 
    global label_last_date 
    global cal

    # Hauptfenster (neue Fenster)
    kalender = Tk()
    kalender.title('Kalender')
    #---------------------------------------------------------------------------------------------#
    frame_kalender = ttk.LabelFrame(kalender, text="Kalender")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    # Kalender
    cal = Calendar(frame_kalender, selectmode="day", year=2021, month=9, day=6)
    cal.grid(column=0, row=0, pady=5, padx=5)
    #---------------------------------------------------------------------------------------------#
    # erstellen einen conatiner für die Info Box
    frame_kalender = ttk.LabelFrame(kalender, text="Infomation")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    info = ttk.Label(frame_kalender, text="Der Zeitraum kann ausgewählt werden zwischen dem:")
    info.grid(column=0, row=0 ,padx=5, pady=5)
    info = ttk.Label(frame_kalender, text= first_string +" und "+ last_string)
    info.grid(column=0, row=1 ,padx=5, pady=5)
    #---------------------------------------------------------------------------------------------#
    # erstellen einen conatiner für die Tasten
    frame_kalender = ttk.LabelFrame(kalender, text="Auswahl")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    # infor erstellen für die auswahl des ersten DAtums
    fi_label = ttk.Label(frame_kalender, text="Erstes Datum bestätigen")
    fi_label.grid(column=0, row=0, padx=5, pady=5)
    # erstellen des Knopfes für das bestätigen des ersten Monats
    my_button= ttk.Button(frame_kalender, text="Bestätigen", command=grab_date_first)
    my_button.grid(column=1 , row=0, pady=5, padx=5)

    label_first_date= ttk.Label(frame_kalender, text="")
    label_first_date.grid(column=0 , row=1, pady=5, padx=5)

    # infor erstellen für die auswahl des ersten DAtums
    fi_label = ttk.Label(frame_kalender, text="Zweites Datum bestätigen")
    fi_label.grid(column=0, row=2, padx=5, pady=5)
    
    my_button= ttk.Button(frame_kalender, text="Bestätigen", command=grab_date_last)
    my_button.grid(column=1 , row=2, pady=5, padx=5)

    label_last_date= ttk.Label(frame_kalender, text="")
    label_last_date.grid(column=0 , row=3, pady=5, padx=5)
    #---------------------------------------------------------------------------------------------#
    frame_kalender = ttk.LabelFrame(kalender, text="Kommandos")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    create_df_date = ttk.Button(frame_kalender, text="Erzeuge Tabelle", command=df_filter_date)
    create_df_date.grid(column=0 , row=0 ,padx=5, pady=5)

    create_df_date = ttk.Button(frame_kalender, text="Zurücksetzen", command=refresh_date_border_label)
    create_df_date.grid(column=1 , row=0 ,padx=5, pady=5)

    KalButton = ttk.Button(frame_kalender, text="Beenden", command=kalender.destroy)
    KalButton.grid(column=2 , row=0 , padx=5, pady=5)