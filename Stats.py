
from logging import info
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
import tkinter as tk
from tkinter.ttk import Combobox
from numpy import left_shift
from numpy.core.fromnumeric import size
import pandas as pd
from pandastable import Table
import matplotlib.pyplot as plot
from scipy.stats import linregress
from tkcalendar import *
import tkinter as tk
from tkinter import ttk
# Browsing the input file
from sympy.stats import independent


# importiere Module aus anderen Dateien
from prep_stats import temp_time, df_timestamp, choose_date_gui, commpare_date_input, firstLast_temp_df, firstLast_humi_df, first_string, last_string
from kalender_window import open_kalender
from datensatz_window import open_datensatz



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
    #if (btnVisual['state'] == tk.DISABLED):
    btnVisual['state'] = tk.NORMAL


# Funktion um die Diagramme darzustellen
def visualizeData():
    # Get the dataset and the visualization option
    opt = str(option.get())
    data = pt.getSelectedDataFrame()

    if data.empty:
        ttk.messagebox.showerror("Data Visualization", "No Data Selected.")
        return

    # To plot the charts and bars we need numerical values only
    numericCols = []

    # Getting the columns which contain numeric values
    cols = data.columns.tolist()
    if (len(cols) < 2):
        ttk.messagebox.showerror("Insufficient Data", "Please Select Minimum Two Columns.")
        return

    for col in cols:
        cells = data[col].tolist()
        dt = type(cells[0])
        if (dt == int or dt == float):
            numericCols.append(col)

    # Visualizing data according to the option
    if (opt == "1"):
        # Streuungsdiagramm
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.scatter(x, y)
        plot.xlabel(numericCols[0])
        plot.ylabel(numericCols[1])
        plot.title('Streuungsdiagramm')
        plot.show()
    elif (opt == "2"):
        # Histogramm
        x = data[numericCols[0]].tolist()
        plot.hist(x, stacked=False)
        plot.xlabel(numericCols[0])
        plot.title('Histogram')
        plot.show()
    elif (opt == "3"):
        # Liniendiagramm
        data.sort_values(by=[numericCols[0], numericCols[1]], inplace=True)
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.plot(x, y)
        plot.xlabel(numericCols[0])
        plot.ylabel(numericCols[1])
        plot.title('Line Plot')
        plot.show()
    elif (opt == "4"):
        # Balkendiagramm
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.bar(x, y, width=0.2)
        plot.xlabel(numericCols[0])
        plot.ylabel(numericCols[1])
        plot.title('Bar Chart')
        plot.show()
    elif (opt == "5"):
        # Boxplot
        x = data[numericCols[0]].tolist()
        y = data[numericCols[1]].tolist()
        plot.pie(y, labels=x)
        plot.xlabel(numericCols[0])
        plot.title('Pie Chart')
        plot.show()


# funktion der Taste "Tablle" um den ausgewählten Zeitraum und den ausgewählten column
def merge_df():
    # df_date (das ausgewählte datum als DataFrame) erst in der Funktion importieren wenn es benötigt wird!
    from kalender_window import df_date
    from datensatz_window import df_gui
    global merged_df

    merged_df = pd.merge(df_date, df_gui , left_index=True, right_index=True)
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


#######################################################################################################################
#######################################################################################################################
def VisualDown():
    from prep_stats import visual_method_dynamic
    from datensatz_window import df_gui, stringChoosen
    #from kalender_window import a
    a = 2
    opt = str(option.get()) # ausgewählte Visualisierungsmethode
    data = merged_df # DataFrame
    print("IN DER FUNKTION")
        # Visualizing data according to the option
    if (opt == "1"):
        # Streuungsdiagramm
        visual_method_dynamic(1,"Temperatur",data, a, stringChoosen)
    elif (opt == "2"):
        # Histogramm
        visual_method_dynamic(4,"Temperatur",data, a, stringChoosen)
    elif (opt == "3"):
        print("IN DER IF ABFRAGE")
        # Liniendiagramm
        visual_method_dynamic(2,"Temperatur",data, a, stringChoosen)########## DIESER WEG FUNKTIONEN ANDERE FUNKTIONEN ANPASSEN !!!!
        plot.show()
##########################################################################################################################################
####################################################################################################################### xxxxx   

    # elif (opt == "4"):
    #     # Balkendiagramm
    #     visual_method_dynamic(4,)

    elif (opt == "5"):
        # Boxplot
        visual_method_dynamic(3,"Temperatur",data, a, stringChoosen)
        














# Beginn der Haupt-GUI
# GUI-Widgets einrichten
root = Tk()
# Titelname des Fensters
root.title("static_py")
# einstellen der Fenstergröße / wenn nicht angegeben wird das Fenster jeweils angepasst
#root.minsize(600, 600)
#root.maxsize(600, 600)
#---------------------------------------------------------------------------------------------#
# erstellen eines Containers für den Titel des Programms
topFrame = Frame(root, width=1350, height=50,bd=4, relief="ridge")# mit bd=4 und relief="ridge" Umrandung des Titels erstellt 
topFrame.pack(side=TOP, fill=X, expand=1, anchor=N)
#---------------------------------------------------------------------------------------------#
titleLabel = ttk.Label(topFrame, font=('arial', 12, 'bold'),
                   text="statistische Auswertung und Visualisierung von Datenbankdaten",
                   anchor=W)
titleLabel.pack(side=TOP)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# übergeordnetes oberes Frame unter dem Titel
über_Frame = ttk.Frame(root)
über_Frame.pack(side=TOP, anchor=W)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# erstelle ersten Frame
fr = ttk.LabelFrame(über_Frame, text="Datensatz hochladen")
fr.pack(side=LEFT, anchor=SW, padx=10, pady=10)
#---------------------------------------------------------------------------------------------#
# Text über dem Browse Button
infoLabel_up = ttk.Label(fr, text='.xlsx/.csv') # (font=('Calibri', 16)) benutze die Funktion um style und schriftgröße
infoLabel_up.grid(column=0, row=0, padx=5, pady=5) # benutze (pady=10) um einen abstand zu dem nächsten block in der y-achse zu halten / dassselbe gilt (padx=10) für x-achse
# erstellen des Browse Buttons
browseBtn = ttk.Button(fr, text='Browse', command=browse)
browseBtn.grid(column=0, row=1, padx=5, pady=5)

#---------------------------------------------------------------------------------------------#
# erstellen ein neuen Frame / rechts
fr = ttk.LabelFrame(über_Frame, text="Datensatz runterladen")
fr.pack(side=LEFT,anchor=SW, padx=10, pady=10)
#---------------------------------------------------------------------------------------------#
infoLabel_do = ttk.Label(fr, text="Zeitraum\nwählen") 
infoLabel_do.grid(column=0, row=0, padx=5, pady=5)

KalenderBtn = ttk.Button(fr, text="Kalender", command=open_kalender)
KalenderBtn.grid(column=0, row=1, padx=5, pady=5)

infoLabel_do1 = ttk.Label(fr, text="Datensatz\nwählen") 
infoLabel_do1.grid(column=2, row=0, padx=5, pady=5)

KalenderBtn = ttk.Button(fr, text="Datensatz", command=open_datensatz)
KalenderBtn.grid(column=2, row=1, padx=5, pady=5)

#---------------------------------------------------------------------------------------------#
# erstellen ein neuen Frame / rechts
fr = ttk.LabelFrame(über_Frame, text="Status")
fr.pack(side=LEFT,anchor=SW, padx=10, pady=10)
#---------------------------------------------------------------------------------------------#

fr2 = ttk.Frame(fr)
fr2.pack(side=TOP,anchor=E, padx=5, pady=5)

checkDate = ttk.Label(fr2, text="Zeitraum:")
checkDate.pack(side=LEFT)

#CheckVarDate=BooleanVar()
checkbuttondate= ttk.Checkbutton(fr2)
checkbuttondate.pack(side=LEFT)

# box_date = Entry(fr2, width=2)
# box_date.configure({"background": "red"})
# box_date.pack(side=LEFT)

fr2 = ttk.Frame(fr)
fr2.pack(side=TOP,anchor=E, padx=5, pady=5)

checkData = ttk.Label(fr2, text="Datensatz:")
checkData.pack(side=LEFT)

CheckVarData=BooleanVar()
checkbuttondata= ttk.Checkbutton(fr2)
checkbuttondata.pack(side=LEFT)

# box_data = Entry(fr2, width=2)
# box_data.configure({"background": "red"})
# box_data.pack(side=LEFT)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# neues übergeordnetes Frame
über_Frame = ttk.Frame(root)
über_Frame.pack(side=TOP, anchor=W)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
fr = ttk.LabelFrame(über_Frame, text="Aktion")
fr.pack(side=LEFT,anchor=SW, padx=10, pady=10)

# Visualisierungstaste erstellen                                                            #####################################################
btnVisual = ttk.Button(fr, text="Visualisierung", command=VisualDown, state=tk.DISABLED) ############################################################ BEI COMMAND WIEDER VISUALIZEDATA 
btnVisual.grid(column=0, row=0 ,padx=5, pady=5)

connButton = ttk.Button(fr, text="Tabellen\nzusammenfügen", command=merge_df)
connButton.grid(column=1, row=0 ,padx=5, pady=5)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# neues übergeordnetes Frame
über_Frame = ttk.Frame(root)
über_Frame.pack(side=TOP, anchor=W)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
fr = ttk.LabelFrame(über_Frame, text="statistische Visualisierung")
fr.pack(side=TOP,anchor=SW, padx=10, pady=10)
#---------------------------------------------------------------------------------------------#
# wird ein Radiobutton angegklickt wird in option der Value-Wert von dem gedrückten RadioButon abgespeichert
# Zusätzlich wird der Visualisierungsbuttton durch den command vom Radiobutton aktiviert
option = IntVar()
r1 = ttk.Radiobutton(fr, text="Streuungs-\ndiagramm", variable=option, value=1, command=enableVis)
r1.grid(column=0, row=0, padx=5, pady=5)
r2 = ttk.Radiobutton(fr, text="Histogram", variable=option, value=2, command=enableVis)
r2.grid(column=1, row=0, padx=5, pady=5)
r3 = ttk.Radiobutton(fr, text="Linien-\ndiagramm", variable=option, value=3, command=enableVis)
r3.grid(column=2, row=0, padx=5, pady=5)
r4 = ttk.Radiobutton(fr, text="Balken-\ndiagramm", variable=option, value=4, command=enableVis)
r4.grid(column=3, row=0, padx=5, pady=5)
r5 = ttk.Radiobutton(fr, text="Boxplot", variable=option, value=5, command=enableVis)
r5.grid(column=4, row=0, padx=5, pady=5)
#---------------------------------------------------------------------------------------------#
fr = ttk.LabelFrame(über_Frame, text="statistische Verfahren")
fr.pack(side=TOP,anchor=SW, padx=10, pady=10)
#---------------------------------------------------------------------------------------------#
################################################################################################################################
################################################################################################################################ ANPASEN STATISTISCHE VERFAHREN VARIABELN AUF DIE AUSWERTUNGEN prep_stats !!!!!!
optionStat = IntVar()
r6 = ttk.Radiobutton(fr, text="standart-\nabweichung", variable=optionStat, value=1)
r6.grid(column=0, row=0, padx=5, pady=5)
r7 = ttk.Radiobutton(fr, text="Median", variable=optionStat, value=2)
r7.grid(column=1, row=0, padx=5, pady=5)
r8 = ttk.Radiobutton(fr, text="Mittel-\nwert", variable=optionStat, value=3)
r8.grid(column=2, row=0, padx=5, pady=5)
r9 = ttk.Radiobutton(fr, text="oberes\nQuantil", variable=optionStat, value=4)
r9.grid(column=3, row=0, padx=5, pady=5)
r10 = ttk.Radiobutton(fr, text="unteres\nQuantil", variable=optionStat, value=5)
r10.grid(column=4, row=0, padx=5, pady=5)
#---------------------------------------------------------------------------------------------#
# neuer container für die Beenden Taste
fr = ttk.Frame(root)
fr.pack(side=TOP, anchor=SW, padx=10, pady=10)
#---------------------------------------------------------------------------------------------#
# Beenden Taste erstellen
btnQuit = ttk.Button(fr, text="Beenden", command=root.destroy)
btnQuit.grid()
##################################################################################################################################################
################################################################################################################################################## PROGRAMMIEREN SODASS DIE TABELLE IN EINEM NEUEN FENSTER ANGEZEIGT WIRD
# Das ist der Frame der die TABELLE ausgibt, die man vorher mit Browse eingelesen hat, in einem Fenster was eingebettet wird.
#---------------------------------------------------------------------------------------------#
frame = ttk.Frame(root)
frame.pack(fill=BOTH)
#---------------------------------------------------------------------------------------------#
# Starting the Tkinter application
root.mainloop()
