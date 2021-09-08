# importiere Bibliotheken
from tkinter import *
from tkinter import messagebox
import pandas as pd
from pandastable import Table
from tkcalendar import *

# importiere Module aus andere Dateien
from prep_stats import temp_time, df_timestamp, choose_date_gui, commpare_date_input, firstLast_temp_df, firstLast_humi_df, first_string, last_string


def quit(x):
    x.destroy()

# funktion wird aktiviert wenn Button OK gedrückt wird
def on_click():
    global df2
    # bekomme das ausgewählte column aus dem OptionMmenu
    val = selected.get()
    #übergege den column in ein neue DataFrame
    df2 = temp_time[f"{val}"]
    df2 = pd.DataFrame(data=df2)
    df2_clear = df2.dropna()
    # neues Fenster erstellen um den ausgewählten Sensor anzuzeigen
    tabelleSens = Tk()
    tabelleSens.title("Tabelle - ausgewählter Sensor")
    #---------------------------------------------------------------------------------------------#
    frame_tabelle_sens = Frame(tabelleSens)
    frame_tabelle_sens.pack(fill=X, side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    pt = Table(frame_tabelle_sens, dataframe=df2_clear)
    pt.show()
    #print(df2)



def open_datensatz():
    global selected

    datensatz = Tk()
    datensatz.title('Datensatz aus der Datenbank wählen')

    #---------------------------------------------------------------------------------------------#
    # erstellen einen conatiner für die Info Box
    fr = Frame(datensatz)
    fr.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    # Auswählen eines columns
    # bekomme die column Namen aus dem DataFrame
    values = list(temp_time) 
    selected = StringVar()
    # erstelln des Infotextes
    info_optionmenu = Label(fr, text="Temperatur-\ndaten wählen")
    info_optionmenu.grid(column=0, row=0, padx=5, pady=5)
    # erstelle einen Button der aufrollt und alle column namen anzeigt die ausgewählt werden können
    options = OptionMenu(fr, selected, *values)
    options.grid(column=0, row=1, padx=5, pady=5)
    # Button zum auswählen des columns
    button = Button(fr, text='Bestätigen', command=on_click)
    button.grid(column=1, row=0, padx=5, pady=5)
    #---------------------------------------------------------------------------------------------#
    fr = Frame(datensatz)
    fr.pack(side=TOP)
    #---------------------------------------------------------------------------------------------#
    KalButton = Button(fr, text="Beenden", command=datensatz.destroy)
    KalButton.grid(column=0 , row=0 , padx=5, pady=5)