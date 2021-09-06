# Author: Aman Verma
# Description: This is a Python Desktop Application which reads the Excel and CSV datasets and
# compute correlation and regression between the data and visualize the data using charts and plots.
# Importing various GUI and data manipulation libraries
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
from prep_stats import temp_time, humi_time

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

    btnCor['state'] = tk.NORMAL
    btnLinReg['state'] = tk.NORMAL
    # Draw the table in case multiple files are being opened using the application
    pt.redraw()
#########################################################################################################################################################################

# For computation of Karl Pearson Correlation with the selected data from the table
def karlCor():
    data = pt.getSelectedDataFrame()
    if data.empty:
        messagebox.showerror("Karl Pearson Correlation (Coefficients)", "Data not Selected.")
    else:
        res = data.corr(method="pearson")
        print(res.to_string())
        # messagebox.showinfo("Karl Pearson Correlation (Coefficients)", res.to_string())
        showCorRes(res.to_string())


# Regression
def linearRegression():
    data = pt.getSelectedDataFrame()

    # Getting the first two numeric data
    numericCols = []
    cols = data.columns.tolist()
    if (len(cols) < 2):
        messagebox.showerror("Insufficient Data", "Please Select Minimum Two Columns.")
        return

    for col in cols:
        cells = data[col].tolist()
        dt = type(cells[0])
        if (dt == int or dt == float):
            numericCols.append(col)

    # Collecting X and Y for Regression
    x = data[numericCols[0]].tolist()
    y = data[numericCols[1]].tolist()

    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    global equation
    equation = "y = " + str(slope) + "*x + " + str(intercept)
    showRegRes(equation, r_value, std_err)


def showRegRes(equation, coefficient, error):
    rootRes = Tk()
    rootRes.title("Regression Result")
    rootRes.minsize(400, 400)
    rootRes.maxsize(800, 400)

    eq = "Regression Equation: " + equation
    coef = "Coefficent: " + str(coefficient)
    err = "Standard Error: " + str(error)
    result = eq.replace("*", "") + "\n" + coef + "\n" + err

    res = Label(rootRes, text=result, font=('Calibri', 14))
    res.pack(pady=15)

    label = Label(rootRes, text='Prediction', font=('Calibri italic', 14))
    label.pack(pady=10)

    label1 = Label(rootRes, text='Independent Variable (x)', font=('Calibri', 12))
    label1.pack(pady=5)

    global independent
    independent = Entry(rootRes)
    independent.pack(pady=5)

    btn = Button(rootRes, text='Predict', command=predictReg)
    btn.pack(pady=5)

    global dependent
    dependent = Label(rootRes, text='', font=('Calibri', 14))
    dependent.pack(pady=5)

    rootRes.mainloop()


def predictReg():
    exp = equation.split("= ")[1]
    exp = exp.replace("x", independent.get())

    res = eval(exp)
    dependent['text'] = "y = " + str(res)


# For displaying the correlation results in a new window with double scroll view
def showCorRes(resStr):
    rootRes = Tk()
    rootRes.title("Correlation Result")
    rootRes.minsize(500, 400)
    rootRes.maxsize(700, 500)

    # Create horizontal and vertical scroll bars
    SVBar = tk.Scrollbar(rootRes)
    SVBar.pack(side=tk.RIGHT, fill="y")
    SHBar = tk.Scrollbar(rootRes, orient=tk.HORIZONTAL)
    SHBar.pack(side=tk.BOTTOM, fill="x")

    # Put the result in the Box
    TBox = tk.Text(rootRes, yscrollcommand=SVBar.set, xscrollcommand=SHBar.set, wrap="none", font=('Consolas', 10))
    TBox.pack(expand=0, fill=tk.BOTH, padx=10, pady=10)
    TBox.insert(tk.END, resStr)

    # Configure the scrollbars
    SHBar.config(command=TBox.xview)
    SVBar.config(command=TBox.yview)

    rootRes.mainloop()


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
    df2 = temp_time[f"{val}"]

    print(df2)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# folgend wurde .pack() durch .grid() Funktion ersetzt / wieder zurückgesetzt
# GUI-Widgets einrichten
root = Tk()
# Titelname des Fensters
root.title('statistische Auswertung mit Python')
# einstellen der Fenstergröße / wenn nicht angegeben wird das Fenster jeweils angepasst
#root.minsize(600, 600)
#root.maxsize(600, 600)

#---------------------------------------------------------------------------------------------#
# Das ist der Frame der die TABELLE ausgibt, die man vorher mit Browse eingelesen hat.
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
browseBtn.pack(side=LEFT)
#---------------------------------------------------------------------------------------------#
# erstellen ein neuen Frame
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
instr = Label(fr, text="Select Data from table and perform following operations")
instr.pack(anchor=W)
# erstellen des Korrelations Taste
btnCor = Button(fr, text="Correlation", command=karlCor, state=tk.DISABLED)
btnCor.pack(side=LEFT)
# erstellen der Regression Taste
btnLinReg = Button(fr, text="Regression", command=linearRegression, state=tk.DISABLED)
btnLinReg.pack(side=LEFT)
# Visualisierungstaste erstellen
btnVisual = Button(fr, text="Visualization", command=visualizeData, state=tk.DISABLED)
btnVisual.pack(side=LEFT)
# Beenden Taste erstellen
btnQuit = Button(fr, text="Beenden", command=root.destroy)
btnQuit.pack(side=LEFT)

#---------------------------------------------------------------------------------------------#
# der container der radiobuttons / untergeordnet von (frameBtn).
fr = Frame(root)
fr.pack(fill=X, side=TOP)
#---------------------------------------------------------------------------------------------#
#bottom_frameBtn = Frame(frameBtn)
#bottom_frameBtn.pack(side=BOTTOM, fill=BOTH)
#---------------------------------------------------------------------------------------------#
# choices = ["scatter plot", "Histogram","line plot","bar plot",]
# variable = StringVar(frameBtn)
# w = OptionMenu(frameBtn, variable, *choices)
# w.pack()

option = IntVar()
r1 = Radiobutton(fr, text="Streuungsdiagramm", variable=option, value=1, command=enableVis)
r1.pack(side= LEFT)
r2 = Radiobutton(fr, text="Histogram", variable=option, value=2, command=enableVis)
r2.pack(side= LEFT)
r3 = Radiobutton(fr, text="Liniendiagramm", variable=option, value=3, command=enableVis)
r3.pack(side= LEFT)
r4 = Radiobutton(fr, text="Balkendiagramm", variable=option, value=4, command=enableVis)
r4.pack(side= LEFT)
#r5 = Radiobutton(frameBtn, text="Pie Chart", variable=option, value=5, command=enableVis) # wird nicht benötigt
#r5.pack(in_=top_frameBtn, side=LEFT)


# Auswählen eines columns
# bekomme die column Namen aus dem DataFrame
values = list(temp_time) 
selected = StringVar()
# erstelle einen Button der aufrollt und alle column namen anzeigt die ausgewählt werden können
options = OptionMenu(root, selected, *values)
options.pack()

button = Button(root, text='OK', command=on_click)
button.pack()

# frame for table and button "Next Data"
frame_data = Frame(root)
frame_data.pack()






# Starting the Tkinter application
root.mainloop()
