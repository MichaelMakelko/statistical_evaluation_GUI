# Author: Aman Verma
# Description: This is a Python Desktop Application which reads the Excel and CSV datasets and
# compute correlation and regression between the data and visualize the data using charts and plots.
# Importing various GUI and data manipulation libraries
from logging import info
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from numpy import left_shift
from numpy.core.fromnumeric import size
import pandas as pd
from pandastable import Table, data
import matplotlib.pyplot as plot
from scipy.stats import linregress
from prep_stats import temp_time, df_timestamp, choose_date_gui, commpare_date_input, firstLast_temp_df, firstLast_humi_df, first_string, last_string
from tkcalendar import *

# Browsing the input file
from sympy.stats import independent

# auswählen einer Datei / wird jedoch nicht benötigt da ich DataFrames verwenden möchte / oder ich erweitere meinen bestehenden Code und speichere die DataFrames in .csv oder excel-dateien
def browse():
    name = str(fd.askopenfilename(filetypes=[('Excel/CSV Files', '*.xlsx; *xls; *.csv')]))
    # If file is selected
    if (name != ""):
        messagebox.showinfo("Selected File: ", name)
        # gehe in die funktion readFile()
        readFile(name)


# Reading the file
def readFile(loc):
    # Object of pandas table
    global pt
    # Read Excel File
    if (loc.endswith('.xlsx') or loc.endswith('.xls')):
        # ausgewählte Datei in ein DataFrame umschreiben
        df = pd.read_excel(loc)
        # Put the data in the table
        pt = Table(frame, dataframe=df, showstatusbar=True, height=200)
        pt.show()
    # Read CSV File
    elif loc.endswith('.csv'):
        # ausgewählte Datei in ein DataFrame umschreiben
        df = pd.read_csv(loc)
        # Put the data in the table
        pt = Table(frame, dataframe=df, showstatusbar=True, height=200)
        pt.show()

    # Draw the table in case multiple files are being opened using the application
    pt.redraw()


# Enable the Visualize button when any radio button is pressed
def enableVis():
    if (btnVisual['state'] == tk.DISABLED):
        btnVisual['state'] = tk.NORMAL


# Funktion um die Diagramme darzustellen
def visualizeData():
    # Get the dataset and the visualization option
    opt = str(option.get())
    data = pt.getSelectedDataFrame()

    if data.empty:
        messagebox.showerror("Data Visualization", "No Data Selected.")
        return

    # To plot the charts and bars we need numerical values only
    numericCols = []

    # Getting the columns which contain numeric values
    cols = data.columns.tolist()
    if (len(cols) < 2):
        messagebox.showerror("Insufficient Data", "Please Select Minimum Two Columns.")
        return

    for col in cols:
        cells = data[col].tolist()
        dt = type(cells[0])
        if (dt == int or dt == float):
            numericCols.append(col)

    # Visualizing data according to the option
    if (opt == "1"):
        # Getting the first two numeric columns for scatter plot
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.scatter(x, y)
        plot.xlabel(numericCols[0])
        plot.ylabel(numericCols[1])
        plot.title('Scatter Plot')
        plot.show()
    elif (opt == "2"):
        # The first numeric column is plotted in histogram
        x = data[numericCols[0]].tolist()
        plot.hist(x, stacked=False)
        plot.xlabel(numericCols[0])
        plot.title('Histogram')
        plot.show()
    elif (opt == "3"):
        # Getting the first two numeric columns for line plot and sorting the data before plotting
        data.sort_values(by=[numericCols[0], numericCols[1]], inplace=True)
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.plot(x, y)
        plot.xlabel(numericCols[0])
        plot.ylabel(numericCols[1])
        plot.title('Line Plot')
        plot.show()
    elif (opt == "4"):
        # Getting the first two numeric columns for bar chart
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.bar(x, y, width=0.2)
        plot.xlabel(numericCols[0])
        plot.ylabel(numericCols[1])
        plot.title('Bar Chart')
        plot.show()
    elif (opt == "5"):
        # The first numeric column is used as label and second numeric column is used in the chart
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.pie(y, labels=x)
        plot.xlabel(numericCols[0])
        plot.title('Pie Chart')
        plot.show()


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
        messagebox.showwarning(title="Warnung", message="Das ausgewählte Datum ist nicht in der Datenbank aufgenommen")
    

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
        messagebox.showwarning(title="Warnung", message="Das ausgewählte Datum ist nicht in der Datenbank aufgenommen")
    

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
    frame_tabelle_date = Frame(tabelle)
    frame_tabelle_date.pack(fill=X, side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    pt = Table(frame_tabelle_date, dataframe=df_date)
    pt.show()
    
def refresh_date_border_label():
    label_first_date.config(text="")
    label_last_date.config(text="")
    quit(tabelle)


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
    frame_kalender = LabelFrame(kalender, text="Kalender")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    # Kalender
    cal = Calendar(frame_kalender, selectmode="day", year=2021, month=9, day=6)
    cal.grid(column=0, row=0, pady=5, padx=5)
    #---------------------------------------------------------------------------------------------#
    # erstellen einen conatiner für die Info Box
    frame_kalender = LabelFrame(kalender, text="Infomation")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    info = Label(frame_kalender, text="Der Zeitraum kann ausgewählt werden zwischen dem:")
    info.grid(column=0, row=0 ,padx=5, pady=5)
    info = Label(frame_kalender, text= first_string+" und "+ last_string)
    info.grid(column=0, row=1 ,padx=5, pady=5)
    #---------------------------------------------------------------------------------------------#
    # erstellen einen conatiner für die Tasten
    frame_kalender = LabelFrame(kalender, text="Auswahl")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    # infor erstellen für die auswahl des ersten DAtums
    fi_label = Label(frame_kalender, text="Erstes Datum bestätigen")
    fi_label.grid(column=0, row=0, padx=5, pady=5)
    # erstellen des Knopfes für das bestätigen des ersten Monats
    my_button= Button(frame_kalender, text="Bestätigen", command=grab_date_first)
    my_button.grid(column=1 , row=0, pady=5, padx=5)

    label_first_date= Label(frame_kalender, text="")
    label_first_date.grid(column=0 , row=1, pady=5, padx=5)

    # infor erstellen für die auswahl des ersten DAtums
    fi_label = Label(frame_kalender, text="Zweites Datum bestätigen")
    fi_label.grid(column=0, row=2, padx=5, pady=5)
    
    my_button= Button(frame_kalender, text="Bestätigen", command=grab_date_last)
    my_button.grid(column=1 , row=2, pady=5, padx=5)

    label_last_date= Label(frame_kalender, text="")
    label_last_date.grid(column=0 , row=3, pady=5, padx=5)
    #---------------------------------------------------------------------------------------------#
    frame_kalender = LabelFrame(kalender, text="Kommandos")
    frame_kalender.pack(side=TOP, pady=10, padx=10, anchor=W)
    #---------------------------------------------------------------------------------------------#
    create_df_date = Button(frame_kalender, text="Erzeuge Tabelle", command=df_filter_date)
    create_df_date.grid(column=0 , row=0 ,padx=5, pady=5)

    create_df_date = Button(frame_kalender, text="Zurücksetz.", command=refresh_date_border_label)
    create_df_date.grid(column=1 , row=0 ,padx=5, pady=5)

    KalButton = Button(frame_kalender, text="Beenden", command=kalender.destroy)
    KalButton.grid(column=2 , row=0 , padx=5, pady=5)

# funktion der Taste "Tablle" um den ausgewählten Zeitraum und den ausgewählten column
def merge_df():
    merged_df = pd.merge(df_date, df2 , left_index=True, right_index=True)
    merged_df = merged_df.dropna()

    # neues Fenster erstellen um die ausgewählten Sensor Tabelle anzuzeigen
    sensGewählt = Tk()
    sensGewählt.title("Tabelle - ausgewählter Zeitraum + ausgewählter Sensor")
    #---------------------------------------------------------------------------------------------#
    frame_tabelle_sens = Frame(sensGewählt)
    frame_tabelle_sens.pack(fill=X, side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    pt = Table(frame_tabelle_sens, dataframe=merged_df)
    pt.show()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# folgend wurde .pack() durch .grid() Funktion ersetzt / wieder zurückgesetzt
# GUI-Widgets einrichten
root = Tk()
# Titelname des Fensters
root.title("static_py")
# einstellen der Fenstergröße / wenn nicht angegeben wird das Fenster jeweils angepasst
#root.minsize(600, 600)
#root.maxsize(600, 600)
# erstellen eines Containers für den Titel des Programms
topFrame = Frame(root, width=1350, height=50,bd=4, relief="ridge")# mit bd=4 und relief="ridge" Umrandung des Titels erstellt
topFrame.pack(side=TOP, fill=X, expand=1, anchor=N)
titleLabel = Label(topFrame, font=('arial', 12, 'bold'),
                   text="statistische Auswertung und Visualisierung von Datenbankdaten",
                   bd=5, anchor=W)
titleLabel.pack(side=LEFT)
#---------------------------------------------------------------------------------------------#
# Das ist der Frame der die TABELLE ausgibt, die man vorher mit Browse eingelesen hat, in einem Fenster was eingebettet wird.
frame = Frame(root)
frame.pack(fill=BOTH)
#---------------------------------------------------------------------------------------------#
# erstelle ersten Frame
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
# Text über dem Browse Button
infoLabel = Label(fr, text='Select Excel/CSV file') # (font=('Calibri', 16)) benutze die Funktion um style und schriftgröße
# anchor verwenden um den text in einem Frame an eine Seite zu knüpfen
infoLabel.pack(anchor=W) # benutze (pady=10) um einen abstand zu dem nächsten block in der y-achse zu halten / dassselbe gilt (padx=10) für x-achse
# erstellen des Browse Buttons
browseBtn = Button(fr, text='Browse', command=browse)
browseBtn.pack(side=LEFT, anchor=N)

# erstelle eine Taste um die Struktur der Datenbank anzuzeigen 

#---------------------------------------------------------------------------------------------#
# erstellen ein neuen Frame
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
instr = Label(fr, text="Select Data from table and perform following operations")
instr.pack(anchor=W)
# Visualisierungstaste erstellen
btnVisual = Button(fr, text="Visualisierung", command=visualizeData, state=tk.DISABLED)
btnVisual.pack(side=LEFT)

#---------------------------------------------------------------------------------------------#
# der container der radiobuttons / untergeordnet von (frameBtn).
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
option = IntVar()
r1 = Radiobutton(fr, text="Streuungsdiagramm", variable=option, value=1, command=enableVis)
r1.pack(side= LEFT)
r2 = Radiobutton(fr, text="Histogram", variable=option, value=2, command=enableVis)
r2.pack(side= LEFT)
r3 = Radiobutton(fr, text="Liniendiagramm", variable=option, value=3, command=enableVis)
r3.pack(side= LEFT)
r4 = Radiobutton(fr, text="Balkendiagramm", variable=option, value=4, command=enableVis)
r4.pack(side= LEFT)

#---------------------------------------------------------------------------------------------#
# neuer container für die auswahl eines columns von Temperatur Sensoren und bestätigen Buttons
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
# Auswählen eines columns
# bekomme die column Namen aus dem DataFrame
values = list(temp_time) 
selected = StringVar()
# erstelln des Infotextes
info_optionmenu = Label(fr, text="Sensor auswählen")
info_optionmenu.pack(anchor=W)
# erstelle einen Button der aufrollt und alle column namen anzeigt die ausgewählt werden können
options = OptionMenu(fr, selected, *values)
options.pack(side=LEFT)
# Button zum auswählen des columns
button = Button(fr, text='Bestätigen', command=on_click)
button.pack(side=LEFT)
#---------------------------------------------------------------------------------------------#
# neue container für Kalender Button
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
KalenderBtn = Button(fr, text="Kalender", command=open_kalender)
KalenderBtn.pack(anchor=W)

connButton = Button(fr, text="Tabelle", command=merge_df)
connButton.pack(pady=10)

#---------------------------------------------------------------------------------------------#
# neuer container für die Tabelle mit ausgewähltem Zeitraum und ausgewähltem Column
frameMerged = Frame(root)
frameMerged.pack(fill=BOTH)
#---------------------------------------------------------------------------------------------#
# neuer container für die Beenden Taste
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
# Beenden Taste erstellen
btnQuit = Button(fr, text="Beenden", command=root.destroy)
btnQuit.pack()

# Starting the Tkinter application
root.mainloop()
