
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
from statistik_window import open_statistik



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
        messagebox.showerror("Data Visualization", "No Data Selected.")
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
    from datensatz_window import df_gui, stringChoosen
    from prep_stats import find_datagap
    global merged_df
    global first_gap_date
    global last_gap_date



    merged_df = pd.merge(df_date, df_gui , left_index=True, right_index=True)
    gap = find_datagap(merged_df, stringChoosen)
    print(gap)
    print(merged_df)
    first_gap_date = gap["gap_dates"].iloc[0]
    last_gap_date = gap["gap_dates"].iloc[1]
    # ändere den text im Output
    change_text()


    merged_df_clear = merged_df.dropna()

    # neues Fenster erstellen um die ausgewählten Sensor Tabelle anzuzeigen
    sensGewählt = Tk()
    sensGewählt.title("Tabelle - ausgewählter Zeitraum + ausgewählter Sensor")
    #---------------------------------------------------------------------------------------------#
    frame_tabelle_sens = Frame(sensGewählt)
    frame_tabelle_sens.pack(fill=X, side=TOP, padx=10, pady=10)
    #---------------------------------------------------------------------------------------------#
    pt = Table(frame_tabelle_sens, dataframe=merged_df_clear)
    pt.show()



# Visualisierungsfunktion von DataFrames aus prep_stats
def VisualDown():
    from prep_stats import visual_method_dynamic
    # stringChoosen übergibt das ausgewählte column als string
    from datensatz_window import stringChoosen, save_number, axeTitle
    # deklarieren einer variable die sagt ob ein Tag oder Zeitraum gewählt wurde
    from kalender_window import a, save_day, save_date_start, save_date_end
    # dekalrieren der Variable ob Temperatur oder Luftfeuchtigkeit ausgewählt wurde
    #save_string

    opt = str(option.get()) # ausgewählte Visualisierungsmethode aus den Radiobuttons
    data = merged_df # DataFrame übergeben
    print(opt)

        # Visualizing data according to the option
    if (opt == "1"):
        # Streuungsdiagramm
        visual_method_dynamic(1,axeTitle,data, a, stringChoosen, save_number, save_day, save_date_start, save_date_end)
    elif (opt == "2"):
        # Histogramm
        visual_method_dynamic(4,axeTitle,data, a, stringChoosen, save_number, save_day, save_date_start, save_date_end)
    elif (opt == "3"):
        # Liniendiagramm
        visual_method_dynamic(2,axeTitle,data, a, stringChoosen, save_number, save_day, save_date_start, save_date_end)

    elif (opt == "4"):
        # Balkendiagramm
        visual_method_dynamic(5,axeTitle,data, a, stringChoosen, save_number, save_day, save_date_start, save_date_end)

    elif (opt == "5"):
        # Boxplot
        visual_method_dynamic(3,axeTitle,data, a, stringChoosen, save_number, save_day, save_date_start, save_date_end)

    # elif (opt == "4"):
    #     # Balkendiagramm
    #     visual_method_dynamic(4,)
        
# reset Taste um die gewählten Daten anzuzeigen
def reset_menu():
    var_info1.set("None")
    var_info2.set("None")
    var_info3.set("None")
    var_info4.set("None")
    var_info5.set("None")
   





def change_text():
    from kalender_window import save_first_date, save_last_date
    from datensatz_window import stringChoosen
    var_info1.set(save_first_date)
    var_info2.set(save_last_date)
    var_info3.set(stringChoosen)
    var_info4.set(first_gap_date)
    var_info5.set(last_gap_date)





# Beginn der Haupt-GUI
# GUI-Widgets einrichten
root = Tk()
# Titelname des Fensters
root.title("Messdatenvisualisierungssoftware")
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

# #---------------------------------------------------------------------------------------------#
# # erstellen ein neuen Frame / rechts
# fr = ttk.LabelFrame(über_Frame, text="Status")
# fr.pack(side=LEFT,anchor=SW, padx=10, pady=10)
# #---------------------------------------------------------------------------------------------#

# fr2 = ttk.Frame(fr)
# fr2.pack(side=TOP,anchor=E, padx=5, pady=5)

# checkDate = ttk.Label(fr2, text="Zeitraum:")
# checkDate.pack(side=LEFT)

# #CheckVarDate=BooleanVar()
# checkbuttondate= ttk.Checkbutton(fr2)
# checkbuttondate.pack(side=LEFT)

# # box_date = Entry(fr2, width=2)
# # box_date.configure({"background": "red"})
# # box_date.pack(side=LEFT)

# fr2 = ttk.Frame(fr)
# fr2.pack(side=TOP,anchor=E, padx=5, pady=5)

# checkData = ttk.Label(fr2, text="Datensatz:")
# checkData.pack(side=LEFT)

# CheckVarData=BooleanVar()
# checkbuttondata= ttk.Checkbutton(fr2)
# checkbuttondata.pack(side=LEFT)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# neues übergeordnetes Frame
über_Frame = ttk.Frame(root)
über_Frame.pack(side=TOP, anchor=W)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
fr = ttk.LabelFrame(über_Frame, text="Diagrammtyp")
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
#---------------------------------------------------------------------------------------------#
# Visualisierungstaste erstellen                                                         
btnVisual = ttk.Button(fr, text="Visualisierung", command=VisualDown, state=tk.DISABLED) 
btnVisual.grid(column=0, row=0 ,padx=5, pady=5)
# Zusammenfüger des ausgewählten Zeitraums mit dem ausgewähltem Sensor
connButton = ttk.Button(fr, text="Tabellen\nzusammenfügen", command=merge_df)
connButton.grid(column=1, row=0 ,padx=5, pady=5)
# auswählen des statistischen Verfahren auf den diagrammtyp
# darauf achten das nicht jedes statistische Verfahren angewendet werden kann
statBtn= ttk.Button(fr, text="statistik\nwählen", command=open_statistik)
statBtn.grid(column=2, row=0 ,padx=5, pady=5)
# zurücksetzen Button erstellen um das untere Anzeigefenster (die geloggten FElder zu reseten)
resetBtn = ttk.Button(fr, text="Zurücksetzen", command= reset_menu)
resetBtn.grid(column=3, row=0 ,padx=5, pady=5)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# neues übergeordnetes Frame für die erste Linie
über_Frame = ttk.Frame(root)
über_Frame.pack(side=TOP, anchor=W)
# erste Linie
fr = Canvas(über_Frame, width=450, height=5)
fr.pack(side=TOP, anchor=W)
fr.create_line(0, 0, 450, 0, fill="black", width=5)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# neues übergeordnetes Frame für die output box zwischen den Abschnittslinien
über_Frame = ttk.Frame(root)
über_Frame.pack(side=TOP, anchor=W)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
fr = ttk.LabelFrame(über_Frame, text="Daten")
fr.pack(side=LEFT,anchor=SW, padx=10, pady=10)
#---------------------------------------------------------------------------------------------#
###############################################################################################
# hier kommen die geloggten daten ein aus zeitraum und welcher datensatz ausgewählt ist sowie ausgewätes statistisches Verfahren auf den Diagrammtypen
# OUTPUT BOX
info_tit1=ttk.Label(fr, text="Datensatz:")
info_tit1.grid(column=0, row=0, padx=5, pady=5)

var_info3 = StringVar()
var_info3.set("None")
info_set_datensatz=ttk.Label(fr, textvariable=var_info3)
info_set_datensatz.grid(column=1, row=0, padx=5, pady=5)


info_tit2=ttk.Label(fr, text="Zeitraum:")
info_tit2.grid(column=0, row=1, padx=5, pady=5)

var_info1 = StringVar()
var_info2 = StringVar()
var_info4 = StringVar()
var_info5 = StringVar()

var_info1.set("None")
info1_set=ttk.Label(fr, textvariable=var_info1)
info1_set.grid(column=1, row=1, padx=5, pady=5)
# setzen des ersten Datum
#info1_set.config(text=saveFirstDate)

inf=ttk.Label(fr, text="bis")
inf.grid(column=2, row=1, padx=5, pady=5)

var_info2.set("None")
info2_set=ttk.Label(fr, textvariable=var_info2)
info2_set.grid(column=3, row=1, padx=5, pady=5)
# setzen des zweiten Datums
#info2_set.config(text=saveLastDate)

info_tit3=ttk.Label(fr, text="Datenlücke:")
info_tit3.grid(column=0, row=3, padx=5, pady=5)

var_info4.set("None")
info2_set=ttk.Label(fr, textvariable=var_info4)
info2_set.grid(column=1, row=3, padx=5, pady=5)

inf2=ttk.Label(fr, text="bis")
inf2.grid(column=2, row=3, padx=5, pady=5)

var_info5.set("None")
info3_set=ttk.Label(fr, textvariable=var_info5)
info3_set.grid(column=3, row=3, padx=5, pady=5)





###############################################################################################
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# neues übergeordnetes Frame
über_Frame = ttk.Frame(root)
über_Frame.pack(side=TOP, anchor=W)
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
# zweite Linie
fr = Canvas(über_Frame, width=450, height=5)
fr.pack(side=TOP, anchor=W)
fr.create_line(0, 0, 450, 0, fill="black", width=5)
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
