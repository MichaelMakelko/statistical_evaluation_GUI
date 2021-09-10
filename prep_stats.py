## Berrechnungs Bibliotheken
# pandas besitzt alle notwendigen Werkzeuge für die transformation unserer Daten"
import pandas as pd # beinhalt z.B. arbeiten mit DataFrames
import numpy as np # beinhalt z.B. arbeiten mit sogenanten Numpy-Arrays
#from scipy import stats
from statistics import stdev # beinhaltet einige statistische Berrechnungs Möglichkeiten
from datetime import datetime as dt  

## Darstellungs Bibliotheken
#import matplotlib.pyplot as plt, matplotlib.font_manager as fm # Visualisierungs Bibliothek
import seaborn as sns # verbesserte Visualisierungs Bibliothek 
import matplotlib.dates as mdates # um verschiedene Achsenbeschriftungen/Achsenwerte vornehmen zu können

# ermöglicht einen unkomplizierten import einer Excel Datei"
import xlrd
import time

# ermglichen das importieren eines modules aus einer anderen Datei / akktualisiert: .ipynb GitHub (https://github.com/ipython/ipynb) -> ist ein spezielles Modul um Datein einfache zu importieren
import sys
import os

## Verbindung zu einer Datenbank herzustellen
import mysql.connector # meist verwendete Bibliothek um Verbindungen zu einer Datenbank Herzustellen
import sqlalchemy # Bibliothek: um eine sogennanten wieder aufrufbaren logger zu erstellen um wiederholt auf eine Datenbank zuzugreifen

# um das einlesen der config.ini Datei zu ermöglichen
import configparser
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Datenbank Verbindung herstellen

# Deklarierung der config Funktion
#config = configparser.ConfigParser()##########################################################################################################################################################
# auslesen der config.ini Datei
#config.read('config.ini')####################################################################################################################################################################

# folgende funktion
#def mysql_logger():#############################################################################################################################################################################
    # verwendet den Inhalt der config.ini Datei 
    # Syntax um auf die Variablen in der Datei zuzugreifen: config['Überschrift']['variable'] 
#    return mysql.connector.connect(host = config['mysqlDB']['host'],################################################################################################################################
#   user = config['mysqlDB']['user'],################################################################################################################################
#    passwd = config['mysqlDB']['pass'],################################################################################################################################
#    db = config['mysqlDB']['db'])################################################################################################################################

# eine Verbindungsvariable deklarieren, um sich jedes Mal in die Datenbank einzuloggen
#connection = mysql_logger()##################################################################################################################################################################
# Maus erstellen / um sich in der Datnebank bewegen zu können
#cursor = connection.cursor()#################################################################################################################################################################

# SQLAlchemy Engine / ermöglicht das automatische runterladen einer Tabelle in einen gesamten DataFrame (pd.read_sql)
# logger Engine erstellen / string wird aus der config.ini bezogen
#engine = sqlalchemy.create_engine(config['engine']['log'])###################################################################################################################################

# folgender Abschnitt lädt alle Daten von dem __schema__: sa_makelko / __Tabelle__: Raummonitoring runter
# lädt alle columns aus der Tabelle Raummonitoring ein einen gesamtes DataFrame
# eine "log"-engine aus der SQLAlchemy ermöglicht auto. runterladen mehrere Tabellen
#df = pd.read_sql("SELECT * FROM Raummonitoring", con = engine)################################################################################################################################

# funktion zum runterladen des DataFrames in eine CSV
#df.to_csv("C:/Users/Benutzt/Desktop/DatabaseData.csv", encoding="utf-8")


## shows all columns in schema raummonitoring 
# selecting everything with * and set not limit with LIMIT 0 
#cursor.execute("SELECT * FROM Raummonitoring LIMIT 0")#####################################################################################################################################
# create a list from columns in Raummonitoring
#column = cursor.description################################################################################################################################################################
# transform list to pandas dataframe
#df_column = pd.DataFrame(column)############################################################################################################################################################

# trennen der Verbindung zur Datenbank
#connection.close()##########################################################################################################################################################################

# Aufbereiten des Datensatzes
## Gruppieren der Datenframes in (_0/_t/_r)

#------------------------------------------------------------------#
# es wurde für die GUI der Teil mit der Datenbank übersprungen aufgrund der rechenzeit / die Positionen mit vielen "#" in der Zeile müssen wieder eingebetete werden
df = pd.read_csv("C:/Users/Benutzt/Desktop/DatabaseData.csv")
#------------------------------------------------------------------#
"""
1. temp_all und humi_all wird aus dem gesamten Dataframe df gefiltert und für sich als eigens DataFrame abgespeichert / alle Temperaturwerte und Feuchtigkeitswerte (ROH) sind abgespeichert
2. desweiteren werden die Zeitstempel aus Temp. und Luftf. in einem Dataframe abgespeichert
3. Temp. und Luftf. mit den variablenendung _value -> sind die Zeitstempel aus dem Datafrmae ausgegliedert worden / so haben wir jetzt die reinen Messwerte.

wichtig!: bei der ausgliederung der Zeitstempel gehen die Zeilen (row) Index-Nummerierungen nicht verloren sodass Sie in der späteren Visualisierung in einem Diagramm wieder zusammen gelegt werden können und jeder Zeitstempel seinen vorherigen Messwert wiederbekommt.

INFO:
- _0: Messwert
- _t: Transmit Zeitstempel (Wann hat das Gerät gesendet)
- _r: Receive Zeitstempel (Wann wurde in Die Datenbank geschrieben)
"""

# 1. Trennen aus dem DataFrame die Columns Temperatur und Luftfeuchtigkeit
temp_all= df.filter(like="temperature", axis=1) # axis=1 means along "columns" / =0 along "rows"
humi_all= df.filter(like="humidity", axis=1)

# 2. filtering all columns with xxxx values temperature and humidity
humi_utc_r = humi_all.filter(like="_r", axis=1)
temp_utc_r = temp_all.filter(like="_r", axis=1)

# 2. filtering all columns with utc values temperature and humidity
humi_utc_t = humi_all.filter(like="_t", axis=1)
temp_utc_t = temp_all.filter(like="_t", axis=1)

# 3. Filtern die sauberen Temperatur Messwerte 
# in diesem Part sollen die sauberen Messwerte gefiltert werden. Es wird immer von innen nach außen gearbeitet.
# aus dem Dataframe temp_all wird eine Liste erstellt die, die columns beinhaltet mit _r. Weiter werden die columns aus der erstellten Liste aus dem Dataframe entfernt und in ein neuen df übergeben. 
temp_value_filter1 = temp_all[temp_all.columns.drop(list(temp_all.filter(like="_r")))]
# gleiches vorgehen nur das jetzt alle column namen mit _t aus dem Dataframe entfernt werden und nurnoch saubere Messwerte in temp_value vorhanden sind
temp_value = temp_value_filter1[temp_value_filter1.columns.drop(list(temp_value_filter1.filter(like="_t")))]

# 3. Filtern die sauberen Luftfeuchtigkeit Messwerte
humi_value_filter1 = humi_all[humi_all.columns.drop(list(humi_all.filter(like="_r")))]
humi_value = humi_value_filter1[humi_value_filter1.columns.drop(list(humi_value_filter1.filter(like="_t")))]

# Filtern den longtime column
stamp = df.filter(like="longtime", axis=1)

## filtern der NaN-Werte
#f"{<variable>}" has brought me the desired result / safes the Dataframe (column) and places as new Dataframe with folowing syntax   
#__WICHTIG!__ -> Syntax von f"{x}" füllt die vorher abgespeicherte variable x in ein String! Das angesprochene x in jedem durchlauf beinhaltet den "column" namen.
# Es musste eine eigen Funktion erstellt werden die von einem DataFrame jedes einzelne Column durchläuft um die NaN Werte zu entferne! / da wenn man diese auf einen DataFrame anwendet wird die gesamte Tabelle gelsöcht aufgrund NaN in jedee Spalte Vorkommen und es aus dem Grundverständnis der Funktion alle entfernet jedoch die gesamte Zeile entfernt!!! auch wenn in der Nächsten Spalte ein Werte in der selben Zeile steht.

# generiert für temp. und luftf. listen in ..._r ..._t ..._0 in die folgenden listen
# Lufetfeuchtigkeits Listen
humi_df_list=[] # relevante Liste für Luftfeuchtigkeits Daten
humi_df_utc_r=[]
humi_df_utc_t=[]

# die for-Schleife durchläuft die columns von dem Dataframe: humi_value in der Variable i
for i in humi_value:
    # speichert in x ein neues DataFrame mit nur den Werten aus dem column i aus humi_value 
    x = pd.DataFrame(humi_value[f"{i}"])
    # löscht in dem column die Zeile mit NaN_werten
    x = x.dropna()
    # fügt abschließend das Dataframe in die liste ein
    humi_df_list.append(x)

for i in humi_utc_t:
    x = pd.DataFrame(humi_utc_t[f"{i}"])
    x = x.dropna()
    humi_df_utc_t.append(x)

for i in humi_utc_r:
    x = pd.DataFrame(humi_utc_r[f"{i}"])
    x = x.dropna()
    humi_df_utc_r.append(x)

# Temperatur Listen
temp_df_list = [] # relevante Liste für Temperatur Daten
temp_df_utc_r = []
temp_df_utc_t = []

for i in temp_value:
    x = pd.DataFrame(temp_value[f"{i}"])
    x = x.dropna()
    temp_df_list.append(x)

for i in temp_utc_r:
    x = pd.DataFrame(temp_utc_r[f"{i}"])
    x = x.dropna()
    temp_df_utc_r.append(x)

for i in temp_utc_t:
    x = pd.DataFrame(temp_utc_t[f"{i}"])
    x = x.dropna()
    temp_df_utc_t.append(x)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# FUnktion um Ausreißer zu entfernen
def temp_filter(x):
    # benötigt das importieren der Bibliotheken die in dieser Funktion Verwendung finden
    from scipy import stats
    import numpy as np
    
    # Für die Spalte wird zunächst der Z-Score jedes Wertes in der Spalte im Verhältnis zum Spaltenmittelwert und zur Standardabweichung berechnet.
    z_scores = stats.zscore(x)
    # Dann wird der absolute Z-Score genommen, denn die Richtung spielt keine Rolle, nur wenn er unter dem Schwellenwert liegt
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3)
    # uhrsprüngliche Dataframe in den Array einfügen
    new_Frame = x[filtered_entries]
    return new_Frame
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# filtern von Ausreißern
# Problem bestand darin, dass kein graph angezeigt wurde aufgrund der gewaltigen änderung des Maßstabes eines Ausßreißers
# Listen für die Daten ohne Ausreißer
temp_value_f=[]
humi_value_f=[]

# Folgende Funktion filtert Ausreißer aus einer Gruppe von Daten
# läufer durch jede zeile in der Liste der Temperaturdaten 
for i in range(0, len(temp_df_list), 1): # len() gibt die länge des Datafrmaes als integer zurück / range(start, ende, läufer)
    x = temp_df_list[i]
    # fügt jeden Column in die Funktion temp_filter() aus der Datei preparation_data
    x_filter=temp_filter(x)
    # fügt anschließend die gefilterte Liste einer neuen Liste an
    temp_value_f.append(x_filter)
    
for i in range(0, len(humi_df_list), 1):
    x = humi_df_list[i]
    x_filter=temp_filter(x)
    humi_value_f.append(x_filter)

## Umwandeln der unix-Zeitstempel in Datum/Uhrzeit
# einen einzelnen Datframe aus "longtime" Daten erstellen
utc_stamp = stamp["longtime"]
# dataframe mit den UTC Werten mit folgender funktion in jahr/monat/tag stunde/minute/sekunde konvertieren
utc_stamp = pd.to_datetime(utc_stamp, unit="ms") # unit einstellen und angeben wie lang der UTC Wert ist um diesen richtig umzurechnen
# einen zusätzlichen Dataframe erstelllen für den manuellen Kalender
df_timestamp = pd.DataFrame({"timestamp": utc_stamp})

# Sortieren der Column namen
temp_df_list.sort(key=str)
temp_df_utc_r.sort(key=str)
temp_df_utc_t.sort(key=str)
temp_value_f.sort(key=str)
humi_df_list.sort(key=str)
humi_df_utc_r.sort(key=str)
humi_df_utc_t.sort(key=str)
humi_value_f.sort(key=str)

## Zusammenfüger der aufbereiteten Daten
# Messwerte sollen wieder mit dem zugehörigen zeitstempel zusammengelegt werden.
# Die Liste der Dataframes wird in ein gesamtes Dataframe erstellt / Jedes Column ist ein Sensor mit Datendf_temp_value
# im folgendem Abschnitt beim zusammenfügen in das gesamte Dataframe, wird auf den Index geachtet. *z.B. hat der Sensor 10 bei dem Index 200 kein Werte aber Sensor 9 schon, dann wird für den Sensor 10 bei dem Index 200 ein NaN Wert eingefügt!

# erstelle aus der Liste von Dataframes: temp_value_f wieder ein gesamtes Dataframe mit Columns der jeweiligen Sensoren und den ursprünglichen Index der Werte 
df_temp_value = pd.concat(temp_value_f, axis=1)
df_humi_value = pd.concat(humi_value_f, axis=1)

#im nächsten Abschnitt wird jetzt das gesamtte Dataframe der aufbereiteten Daten mit der aufgenommenen Zeit zusammengelegt. Dabei wird nur auf den Index geschaut, das heißt dass der Zeitstempel mit dem jeweiligen Index auch an den zugehörigen Index im Dataframe hinterlegt wird.
# legt die aufbereiteten Daten mit den zugehörigen Zeitstempeln zusammen
# gesamtes Dataframe der Temperatursensoren
temp_time = pd.merge(utc_stamp,df_temp_value, left_index=True, right_index=True)
# gesamtes Dataframe der Luftfeuchtigkeitssensoren
humi_time = pd.merge(utc_stamp,df_humi_value, left_index=True, right_index=True)

# Kalender erstellen
# folgender Abschnitt dient zu erstellung eines Kalenders in Tag/Monat/Jahr/Stunde/Minute separat in Spalten getrennt wird. Behält jedoch den Uhrsprünglichen Index bei.
# folgender Abschnitt wurde mithilfe der Seite programmiert: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html / Header: Set logic on the other axes / Verwendet wurde "join=outer" ist in der Syntax werks eingestellt.
# trennen des Zeitstempels in Tag/Monat/Jahr/Stunde/Minute
# aus dem Dataframe wurde manuell jahr/monat/tag/stunde/minute getrennt und ein ein neu erstelles Series(eindimensionale Liste) eingefügt
# aus dem Dataframe utc_stamp wird folgend nur das jahr in ein Series "Jahr" eingefügt usw. mit monat/tag/stunde/minute
df["year"] = pd.DatetimeIndex(utc_stamp).year
df["month"] = pd.DatetimeIndex(utc_stamp).month
df["day"] = pd.DatetimeIndex(utc_stamp).day
df["hour"] = pd.DatetimeIndex(utc_stamp).hour
df["minute"] = pd.DatetimeIndex(utc_stamp).minute
# erstellen von einem Dataframe und fügen die Series-daten dort ein
df_year = pd.DataFrame({"year": df["year"]})
df_month = pd.DataFrame({"month": df["month"]})
df_day = pd.DataFrame({"day": df["day"]})
df_hour = pd.DataFrame({"hour": df["hour"]})
df_min = pd.DataFrame({"minute": df["minute"]})
# folgend werden die oben erstellten Dataframes in ein gesamtes Dataframe eingefügt, sodass tag/monat/jahr/stunde/minute eigene columns sind.
df_cal= pd.concat([df_day, df_month, df_year, df_hour, df_min], axis=1)

# erstellen der automatischen Anzeige der Jahre in dem Titel des Plots
# in min_year wird das erste Jahr abgespeichert, des ersten Messwertes der aufgenommen wurde.
min_year = df_cal["year"].loc[0]
# in dem Dataframe df_cal"year" werden alle jahre größer min_year aufgenommen
df_a = df_cal[df_cal["year"] >= min_year]
# der größte integer wird als max_year festgehalten
max_year = max(df_a["year"])
# zählt die Monate in welchen Daten aufgenommen wurde. Desweiteren wird in jedem Monat gezählt wieviel Messwerte aufgenommen wurden.
month_counts = df_cal["month"].value_counts().sort_index()

# nicht jeder Monat hat notwendigerweise eine Temperatur/Luftfeuchtigkeit, also füllen Sie die fehlenden Monate mit Nullwerten aus
# zeigt auch an, in welchen Monaten die Daten archiviert wurden
date_range = pd.date_range(start=min(df_timestamp['timestamp']), end=max(df_timestamp['timestamp']), freq='D')

# im folgenden wurde die plot Funktion von der Bibliothek pandas angewendet. Diese ist speziell auf das arbeiten mit Dataframes optimiert.
# folgend wurden Funktionen geschrieben die alle Temperaturdaten oder Luftfeuchtigkeitsdaten in einem Streudiagramm anzeigen

# alle 18 Temperaturdaten in einem Diagramm
# zu anfang wird eine varibale deklariert die sozusagen als Bild dient, in diesem Fall: ax / ebenso werden in ax alle Einstellungen für den plot deklariert
def showAllTemp(temp_time, temp_value):
    ax = temp_time.plot(x ="longtime", y="temperature_ers_lite_1_wermser_0_elsys_0",kind="scatter",figsize=(40, 15),title="Temperature - Sensore - Data", lw=0.1, color="C1")
    # läufer Deklarieren der in der folgenden for-Schleife immer um 1 inkrementiert wird, diser dient um eine neue Farbe für Sensoren zu übergeben
    b=1
    # for-Schleife durchläuft die column namen des DataFrames temp-value und fügt Sie in die Y-Achse ein jeweils über den longtime
    for i in temp_value:
        # der name des jeweiligen columns i wird in einen String umgewandelt und auf der Y-Achse als Referenzwert über der X-Achse gelegt
        # Einstellungen des plots werden in ax übergeben
        temp_time.plot(x ="longtime", y=f"{i}", kind="scatter", ax=ax, color="C"+f"{b}")
        # um 1 inkrementieren
        b +=1

### alle 18 Luftfeuchtigkietsdaten in einem Diagramm
def showAllHumi(humi_time, humi_value):
    ax = humi_time.plot(x ="longtime", y="humidity_ers_lite_1_wermser_0_elsys_0",kind="scatter",figsize=(40, 15),title="Luftfeuchtigkeit - Sensore - Data", lw=0.1, color="C1")
    b=1
    for i in humi_value:
        humi_time.plot(x ="longtime", y=f"{i}",kind="scatter", ax=ax ,color="C"+f"{b}")
        b +=1

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Funktionen
## Funktion: Auswahl bestimmter Daten aus der Datenbank
# pick_DataFrame() gibt zurück:
# - Tempeartur- oder Luftfeuchtigkietsdaten ausgewählt (DataFrame)
# - ausgewählten Sensor (Series/DataFrame)
# - Column-namen des Sensors (String)

# filtered values of temperature and humidity /
# df_temp_value
# df_humi_value
# info: got 18 Sensorsets

# 1. wich Data you want ? TempData or HumiData
# 2. shows the DataFrame of the set / chose wich DataSet you want from the Sensors
# 3. safes the DataFrame in new working DataFrame

# WIRD NICHT VERWENDET AUFGRUND DES COLUMN
#############################################################################################################################################################################################
#############################################################################################################################################################################################
# def pick_DataFrame():
#     #global safeDataFrame
    
#     # initialisiere globale variablen
#     global pickd_column_df
#     global a
#     global pick_column
#     global save_string
#     # x a muss vorher angesprochen werden
#     x = int
    
#     # solange 1 oder 2 nicht eingegeben wird, wird der input() wiederholt
#     while x != "1" or "2":
#         # eingabe der zu analisiernenden Tabelle Temperatur(1) oder Luftfeuchtigkeit(2)
#         x = input("wählen Sie zwischen Temperatur- oder Luftfeuchtigkeitsdaten \n geben Sie (1) für Temperaturdaten ein \n geben Sie (2) für Luftfeuchtigkeitsdaten ein \n bestätigen Sie Ihre eingabe mit Enter \n")
        
#         # abfrage der Eingabe
#         # Übergabe der variablen der ausgewählten liste
#         if x == "1":
#             # abspeichern der Liste mit allen Temperatur Sensoren 
#             safeDataFrame = temp_df_list
#             # string für das ausgewählte Temperatur Dataframe
#             a = "Temperatur"
#             var = df_temp_value
#             print("Die ausgewählte Kategorie der Daten ist Temperatur")
#             print("Es werden alle Temperatur-Sensoren aus der Datenbank aufgelistet:")
#             # sens_counter zählt die vorhandenen Sensoren in der Datenbank
#             sens_counter = 0
#             # schleife um die columns in temp_value zu zählen
#             for i in temp_value.columns:
#                 sens_counter += 1
#                 print(i) 
#             break
        
#         # gleiche Erklärung für die Luftfeuchtigkeit
#         if x == "2":
#             a = "Luftfeuchtigkeit"
#             safeDataFrame = humi_df_list
#             var = df_humi_value
#             print("Die ausgewählte Kategorie der Daten ist Luftfeuchtigkeit")
#             print("Es werden alle Luftfeuchtigkeits-Sensoren aus der Datenbank aufgelistet:")
#             sens_counter = 0
#             for i in humi_value.columns:
#                 sens_counter += 1
#                 print(i)
#             break
        
#         # falls die eingabe nicht 1 oder 2 war ist die eingabe ungültig
#         else:
#             print("Die eingabe ist unzulässig")
            
                    
#     # abfrage welcher Sensor ausgewählt werden soll
#     pick_column = input(("Sie können zwischen "+f"{sens_counter} "+ a +" Sensoren einen Datensatz wählen \n gebe Sie nur die Nummer des Sensors ein und bestätigen Sie mit Enter \n"))
    
    
# #     # auf die Sensoren Begrenzen die vorhanden sind
# #     flag_sens= False
# #     while flag_sens != True:
# #         pick_colum = input("Geben Sie die Nummer des Sensors erneut ein \n")
        
# #         if pick_column > sens_counter or pick_column < sens_counter:
# #             flag_sens = False
# #         else:
# #             print("Dieser Sensor existiert nicht")
# #             flag_sens = True
    
    
    
    
#     # dementsprechend wird dieses column ausgewählt
#     pickd_column_df = var.filter(like="_"+f"{pick_column}"+"_", axis=1)
#     # ausgabe des Sensors
#     print("Sie haben folgende Tabelle ausgewählt: \n", pickd_column_df)
#     # folgende Schleife dient zum abspeichern des column namens für weitere Funktionen / falls eine bessere Möglichkeit gefunden wird den Namen abzuspeichern wird die Funktion ersetzt
#     for i in pickd_column_df:
#         x = i
#         save_string = f"{x}"


#############################################################################################################################################################################################
#############################################################################################################################################################################################

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# speichert das erste und letzte Datum als DataFrame ab für die Funktion sartEnd_df()
# first and last data from temp_time
# speichert in folgenden DataFrame ersten und letzten eintrag ab
firstLast_temp_df = pd.concat([temp_time.head(1), temp_time.tail(1)])
# first and last data from humi_time
firstLast_humi_df = pd.concat([humi_time.head(1), humi_time.tail(1)])

# die folgende Funktion soll anzeigen, wann die ersten und letzten Daten in der Datenbank gespeichert wurden / um dem Benutzer zu zeigen, welchen Bereich er auswählen kann
def startEnd_df():
    print("erster und letzter aufgenommene Messwert der Temperaturdaten:")
    print(firstLast_temp_df["longtime"])
    print("erster und letzter aufgenommene Messwert der Luftfeuchtigkeitsdaten:")
    print(firstLast_humi_df["longtime"])
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def statistic_funcion_dynamic(optionStat, merged_df, save_string):
    # benötigt das importieren der Bibliotheken die in dieser Funktion Verwendung finden 
    # eingabe welches statistische Verfahren angewendet werden soll
    #x = input("waehlen Sie ein statistisches Verfahren: \n 1. ahritmetischer Mittelwert \n 2. Standartabweichung \n 3. Median \n 4. unteres Quantil\n 5. oberes Quantil \n 6. Tabelle mit allen Methoden \n Geben Sie die Nummer der Methode ein \n bestaetigen Sie mit Enter\n ")
    
    # aufgrund des DataFrames müssen wir auch das column ansprechen da es kein sauberes Series ist
    if optionStat == "3":
        ergebnis = np.mean(merged_df[f"{save_string}"])
        print("Der ahrithmetische mittelwert ist:", ergebnis)
        return (ergebnis)
    
    if optionStat == "1":
        ergebnis = np.std(merged_df[f"{save_string}"])
        print("Die Standartabweichung ist:", ergebnis)
        return (ergebnis)
    
    if optionStat == "2":
        ergebnis = np.median(merged_df[f"{save_string}"])
        print("Der Median ist:", ergebnis)
        return (ergebnis)
    
    if optionStat == "5":
        ergebnis = np.quantile(merged_df[f"{save_string}"], 0.25)
        print("Das untere Quantil ist:", ergebnis)
        return(ergebnis)
    
    if optionStat == "4":
        ergebnis = np.quantile(merged_df[f"{save_string}"], 0.75)
        print("Das obere Quantil ist:", ergebnis)
        return(ergebnis)
    
    if optionStat == "6":
        ergebnis1 = np.quantile(merged_df[f"{save_string}"], 0.25)
        ergebnis2 = np.median(merged_df[f"{save_string}"])
        ergebnis3 = np.std(merged_df[f"{save_string}"])
        ergebnis4 = np.mean(merged_df[f"{save_string}"])
        ergebnis5 = np.quantile(merged_df[f"{save_string}"], 0.75)
        
        
        df= pd.DataFrame({"Statistische Verfahren" : ["Median","Standartabweichung","ahrithmetischer Mittelwert","oberes Quantil", "unteres Quantil"], "Ergebniss" : [ergebnis2, ergebnis3, ergebnis4, ergebnis5, ergebnis1]})
        print(df)
        #return(df)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
## Funktion: Datumsauswahl oder Datumbereich eines Sensors
# choose_date() gibt zurück:
# - ausgewählten Tag oder Bereich (als DataFrame)
# choose_date() beinhaltet die Funktion commpare_date_input(compare_value) welche prüft automatisch prüft ob der eingebene Tag oder Bereich in dem in der Datenbank aufgenommenen Bereich liegt

# def choose_date(utc_stamp):
#     # deklarierend er globalen Variabeln
#     global filtered_df_raw
#     global filtered_df_date
#     global input_day
#     global final_flag
#     global input_a
#     global input_beginn
#     global input_end
#     # Funktion pick_DataFrame() wird vorher angesprochen
   
#     print("Sie können ein Datum oder einen Zeitraum innerhalb der oben genannten Grenzen wählen.")
#     print("Geben Sie (1) für ein bestimmtes Datum ein. \n Geben Sie (2) für einen Zeitraum ein \n bestätigen Sie anschließend mit Enter ") 
#     # ansprechen der Variabel input_a nötig
#     input_a = int
#     # solange 1 oder 2 nicht eingegeben wird, wird die eingabe wiederholt 
#     while input_a != "1" or "2":
        
#         input_a = input()
        
#         # eingabe für ein bestimmten Tag ausgewählt
#         if input_a == "1":
#             # Ausgabe um einen bestimmten Tag auszuwählen
#             print("Geben Sie jetzt das Datum ein \n Geben Sie in der folgenden Folgenden Reihenfolge ein \n Jahr-Monat-Tag und bestätigen Sie anschließend mit Enter")
#             # erstelle den Merker für das prüfen ob das Datum in dem aufgenommenen Datenbereich liegt
#             final_flag = False
            
#             while final_flag == False:
#                     # eingeben des tages in der Folge: jahr-monat-tag
#                     input_day = input()
#                     # überprüfende Funktion ob der eingegeben tag in dem Datenberreich liegt
#                     compare_value = input_day
#                     # folgende Funktion setzt den final_flag=True falls der Tag in dem Bereich der aufgenommenen Daten liegt
#                     # falls der tag nicht in dem Bereich der aufgenommenen Daten Liegt wird final_flag=Flase aus der Funktion zurückgegeben und eingabe soll wiederholt werden
#                     commpare_date_input(compare_value)
                    
#             # verwenden die pandas .loc funktion mir einer abfrage im Datafr5ame der dann den Tag filtert   
#             filtered_df_raw = utc_stamp.loc[(utc_stamp >= f"{input_day}"+" 00:00:00") & (utc_stamp <= f"{input_day}"+" 23:59:59")]
#             # speichere den Tag in ein Dataframe
#             filtered_df_date = pd.DataFrame({"longtime": filtered_df_raw})
#             # gebe das DataFrame zurück und verlasse die Funktion
#             return filtered_df_date

#         # eingabe für einen Bestimmten Bereich eingegeben
#         if input_a == "2":
#             # Ausgabe um den Bereich auszuwählen
#             print("Geben Sie jetzt den Zeitraum ein \n Geben Sie in der folgenden Folgenden Reihenfolge ein \n Jahr-Monat-Tag und bestätigen Sie anschließend mit Enter")
#             # erstelle den Merker für das prüfen ob das Datum in dem aufgenommenen Datenbereich liegt
#             final_flag = False
#             while final_flag == False:
#                     input_beginn = input("Geben Sie den Beginn des Zeitraumes ein \n")
#                     compare_value = input_beginn
#                     commpare_date_input(compare_value)
                    
#             # final_flag muss zurückgesetzt werden da noch das einzuschließende Datum eingegeben werden muss
#             final_flag = False
            
#             while final_flag == False:
#                     input_end = input("Geben Sie das Ende des Zeitraumes ein \n")
#                     compare_value = input_end
#                     commpare_date_input(compare_value)
                    
#             # die eingabe wird übergeben
#             filtered_df_raw = utc_stamp.loc[(utc_stamp >= f"{input_beginn}") & (utc_stamp <= f"{input_end}")]
#             # gefilterter Berreich wird in einen neuen DataFrame abgespeichert
#             filtered_df_date = pd.DataFrame({"longtime": filtered_df_raw})
#             # abschleißend wird das DataFrame zurückgegeben und die Funktion verlassen
#             return filtered_df_date
        
#         # falls die Eingabe nicht 1 oder 2 war    
#         else:
#             print("Die Eingabe ist unzulässig")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def choose_date_gui(saveFirstDate, saveLastDate):
    # deklarierend er globalen Variabeln
    global filtered_df_raw
    global filtered_df_date
    # verwenden die pandas .loc funktion mir einer abfrage im Datafr5ame der dann den Tag filtert   
    filtered_df_raw = utc_stamp.loc[(utc_stamp >= f"{saveFirstDate}"+" 00:00:00") & (utc_stamp <= f"{saveLastDate}"+" 23:59:59")]
    # speichere den Tag in ein Dataframe
    filtered_df_date = pd.DataFrame({"longtime": filtered_df_raw})
    # gebe das DataFrame zurück und verlasse die Funktion
    return filtered_df_date
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# vorzubereitende Variablen für die Funktion commpare_date_input()
# den letzten Index des DataFrame speichern
lastIndexTemp =temp_time.index[-1]
lastIndexHumi =humi_time.index[-1]
# das erste und letzte Datum in ein Datafrmae speichern
df_first_date = pd.DataFrame(data=firstLast_temp_df, columns=["longtime"], index=[0])
df_last_date = pd.DataFrame(data=firstLast_temp_df, columns=["longtime"], index=[lastIndexTemp])

# erstes Datum welches in die Datenbank geschrieben wurde in einen String umwandeln
first_string = df_first_date.to_string(header=False, index=False, index_names=False)
# letztes Datum welches in die Datenbank geschrieben wurde in einen String umwandeln
last_string = df_last_date.to_string(header=False, index=False, index_names=False)

#################################################################################################################################################################
# Folgender part dient jetzt den ersten und letzten string (die das Datum und Uhrzeit beinahlten) aufzubereiten                                                 # 
# aufzubereiten in diesem part heißt das jahr/tag/monat in separate variabeln in dem datentyp string abzuspeichern und diese später in einen Integer zu wandeln #
# um diesen Integer später als verlgeich nutzen können                                                                                                          #
#################################################################################################################################################################
# dieser Weg wurde gewählt da sonst keine andere Möglichkeit bestand aus dem ausgenommenen Datum im "longtime" column als verlgiechwert zu nutzen.              #
# um letztendlich den Sinn zu verwirklichen das eingegeben Datum zu prügen ob es in dem Berreich der aufgenommenen Daten aus der Datenbank liegt                #
#################################################################################################################################################################
                        
# die Uhrzeit aus der Zeichenkette löschen
first_string = first_string[:-9]
last_string = last_string[:-9]

# FIRST DATE
# Lösche von einem String ende und anfang Syntax: [start:ende] um das Jahr zu erhalten
first_year = first_string[:-6]
# mache aus dem String ein Integer
first_year = int(first_year)
first_month= first_string[5:-3]
first_month = int(first_month)
first_day = first_string[8:]
first_day = int(first_day)
# LAST DATE
last_year = last_string[:-6]
last_year = int(last_year)
last_month= last_string[5:-3]
last_month = int(last_month)
last_day = last_string[8:]
last_day = int(last_day)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
## Funktion: Prüfung ob eingegebenes Datum sich innerhalb des Datenbereichs der Datenbank befindet
# Automatische Prüfung des eingegebenen Datum aus der Funktion choose_date()

def commpare_date_input(compare_value):
    # deklariere die globalen variablen
    global final_flag
    
    # das eingegebene Datum aus choose_date() muss aufbereitet werden und in einzelne Variabeln abgespeichert werden
    # Lösche von einem String ende und anfang Syntax: [start:ende] um das Monat zu erhalten
    compare_value_year = compare_value[:-6]
    # mache aus dem String ein Integer
    compare_value_year = int(compare_value_year)
    compare_value_month= compare_value[5:-3]
    compare_value_month = int(compare_value_month)
    compare_value_day = compare_value[8:]
    compare_value_day = int(compare_value_day)
    
#############################################################################################################################################
# folgend sind nur 3 if-Abfragen notwendig um zu prüfen ob das eingegeben Datum in dem vorgegeben Bereich liegt                             #
# 1. wenn das eingegeben jahr zwischen dem ersten und letzten jahr liegt ist jedes Datum mögliche                                           #
# 2. wenn das erste jahr eingegeben wurde müssen die eingegebenen monat und tag größer sein als die von der ersten eingetragenen Messdate   #
# 3. dasselbe gilt für das letzte jahr                                                                                                      #
#############################################################################################################################################
    
    # 1.)
    # Wenn das eingegeben Jahr größer dem Jahr des ersten eintrages ist und kleiner des Jahres der letzten aufgenommenen Messung    
    if compare_value_year > first_year and compare_value_year < last_year:
        # final_flag dient zur bestätigung das, dass eingegebene Datum die while() schleife der Funktion choose_date passieren kann
        final_flag = True
        # gebe final_flag zurück
        return final_flag
    
    # 2.)
    # falls das eingegeben jahr gleich dem jahrt ist der ersten aufgenommenen Messung ist es wichtig das dieser dann auch den Moant und dem Tag entspricht und nicht unterschreitet
    if compare_value_year == first_year:
        pass
        if compare_value_month >= first_month:
            pass
            if compare_value_day >= first_day:
                final_flag = True
                # gebe final_flag zurück
                return final_flag
    
    # 3.)
    # falls das eingegeben jahr gleich dem jahrt ist der letzten aufgenommenen Messung ist es wichtig das dieser dann auch den Moant und dem Tag entspricht und diesen nicht überschreitet       
    if compare_value_year == last_year:
        pass
        if compare_value_month <= last_month:
            pass
            if compare_value_day <= last_day:
                final_flag = True
                # gebe final_flag zurück
                return final_flag
    
    if compare_value_year > last_year:
        print("das Datum ist nicht zulässig!")
    
    else:
        print("das Datum ist nicht zulässig!")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
## Funktion: Datenlücke finden / prüfen ob es sich wirklich um eine Datenlücke handelt
# Funktion die alle Daten des Sensors durchläuft und erwähnt in welchem die größte Datenlücke herrscht
def find_datagap(choosen_merged, save_string):
    # Folgende Funktion wirft den Dataframe aus und ersetzt in NaN die Länge der aufeinanderfolgenden NaN bis zum nächsten Wert / Datenwerte werden in 0 repräsentiert
    streaks = choosen_merged[f"{save_string}"].isnull().groupby(choosen_merged[f"{save_string}"].isnull().ne(choosen_merged[f"{save_string}"].isnull().shift()).cumsum()).transform(sum)
    # indices enthält die größten aufeinanderfolgenden NaN-Indizes (Anfang-Ende) der Gruppe
    indices = choosen_merged[streaks==streaks.max()].index
    # sicher den ersten Index der Gruppe
    int1 = indices[0]
    # sicher den letzten Index der Gruppe
    int2 = indices[-1]
    # speichere das Datum der Indizes in eine variable ab
    first_date_gap = choosen_merged["longtime"].loc[int1]
    last_date_gap = choosen_merged["longtime"].loc[int2]
    

    ##########################################################
    # prüfen ob die Datenlücke wirklich eine Datenlücke ist !#
    ##########################################################
    # der Index gibt an wo sich NaN-Werte befinden
    na_groups = choosen_merged[f"{save_string}"].notna().cumsum()[choosen_merged[f"{save_string}"].isna()]
    # zählt die aufeinanderfolgenden NaN-Werter nach einem nicht NaN-Wert zusammen
    lengths_consecutive_na = na_groups.groupby(na_groups).agg(len)
    # gibt den größten aufeinanderfolgenden NaN-Wert als integer aus!
    longest_na_gap = lengths_consecutive_na.max()
    # in einen Dataframe umwandeln
    df_check = pd.DataFrame(data=lengths_consecutive_na)
    # namen des Columns änder da dieser gleich dem Index ist (FEHLERBEHEBUNG)
    df_a= df_check.rename(columns={f"{save_string}":"value"})
    # zählt wie oft gruppierte aufienanderfolgedne Werte wiederholt vorkommen!
    df_b = df_a.pivot_table(index=["value"] , aggfunc='size')
    # prüft ob sich der größte aufienanderfolgende Wert sich wiederholt!
    # wenn der höchste aufeinanderkommende Wert nur einmal in dem DataFrame df_b vorkommt gibt es eine Datenlücke!
    if df_b[longest_na_gap] == 1:
        print("Datenlücke gefunden!")
        print("Beginn der Datenlücke:", first_date_gap ," ende der Datenklücke: ", last_date_gap)
    # den wenn isch der größte aufeinanderfolgende-Wert sich wiederholt ist dieser keine Datenlücke! sondern lediglich der die Zeit wonach der Sensor einen Wert leifert.    
    if df_b[longest_na_gap] > 1:
        print("keine Datenlücke gefunden")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#visual_method_dynamic() gibt zurück:
# - plot
#     - X-Achse beinhaltet das ausgewählte Datum oder Bereich
#     - Y-Achse beinhaltet den ausgewählten Sensor
# - es kann zwischen 4 Diagrammen ausgewählt werden
def visual_method_dynamic(x , a_string, choosen_merged, a_int, save_string, pick_column, df_date, input_beginn, input_end):
    import matplotlib.pyplot as plt, matplotlib.font_manager as fm

    # Visualisierung
    # matplotlib.font_manager from https://github.com/gboeing/data-visualization/blob/main/lastfm-listening-history/lastfm_analysis.ipynb
    # Einstellung für die Darstellung des plots
    family = 'DejaVu Sans'
    label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
    title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
    
        
    # START Einstellungen für das Streuungsdiagramm
    if x == 1:
        
        ax = choosen_merged.plot(x ="longtime" , y=save_string , kind="scatter" ,figsize=[15, 5], linewidth=0.1, alpha=0.6, color="#003399")
        ax.yaxis.grid(True)
        # falls nötig ein Limit für die y-achse zu setzten
        #ax.set_ylim((0,50))
        # Einstellungen für die Achsenbeschriftung
        ax.set_ylabel(a_string, fontproperties = label_font)
        
        # stelle die Einstellungen für den plot ein um nur die Zeiteinheit auf der x-Achse anzuzeigen
        if a_int == 1:
            timeFmt = mdates.DateFormatter('%H:%M:%S')
            ax.xaxis.set_major_formatter(timeFmt)
            plt.xticks(rotation=45)
            ax.set_xlabel("Stunden", fontproperties = label_font)
            ax.set_title("Sensor: "+f"{pick_column}"+" Streuungsdiagramm "+ f"{df_date}", fontproperties=title_font) 
        else:
            ax.set_xlabel("Datum", fontproperties = label_font)
            ax.set_title("Sensor: "+f"{pick_column}"+" Streuungsdiagramm, von {} bis {}".format(input_beginn, input_end), fontproperties=title_font)
        plt.show()
        # einsetzen der Jahre (min and max)
        # sowie Einstellungen für die Achsenbeschriftung
#"""----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""            
    # START Einstellungen für das Liniendiagramm
    if x == 2:
        # das Liniendiagramm kann nur angezeigt werden wenn in dem Dataframe keine NaN-Werte vorhanden sind
        drop_na = choosen_merged.dropna()
        print("IN DER ANDEREN DATEI")
        
        ax = drop_na.plot(x ="longtime", y=save_string, kind="line" ,figsize=[15, 5], linewidth=0.5, alpha=0.8, color="#003399")
        ax.yaxis.grid(True)
        #ax.set_ylim((0,50))
        ax.set_ylabel(a_string, fontproperties = label_font)
        if a_int == 1:
            # stelle die Einstellungen für den plot ein um nur die Zeiteinheit auf der x-Achse anzuzeigen
            # setzt aus dem column "longtime" (UTC) unten folgende Syntax / rausgenommen wird stunde/minute/sekunde aus dem gesamten Datum/Uhrzeit
            timeFmt = mdates.DateFormatter('%H:%M:%S')
            ax.xaxis.set_major_formatter(timeFmt)
            # Achsenbeschriftung um 45 grad drehen
            plt.xticks(rotation=45)
            # Den Tag als titel für die x-achse angeben
            ax.set_xlabel("Stunden", fontproperties = label_font)
            # ausgewählten Tag für den Titel verwenden
            ax.set_title("Sensor:"+f"{pick_column}"+" Liniendiagramm "+ f"{df_date}", fontproperties=title_font)
        else:
            ax.set_xlabel("Datum", fontproperties = label_font)
            #ax.set_title("Sensor:"+f"{pick_column}"+" Liniendiagramm, von {} bis {}".format(input_beginn, input_end), fontproperties=title_font)
        plt.show()
                
#"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""            
        # START Einstellungen für das Boxplot
        if x == 3:
            print("Boxplot vom ",a_string ,"-Sensor:", pick_column)
            # plot Settings
            ax = choosen_merged.boxplot()
            ax.set_title(f"{a_string}"+" Sensor: "+f"{pick_column}")
            #ax.set_xlabel("x_label")
            ax.set_ylabel(f"{a_string}")
#"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""             
        # START Einstellungen für das Histogramm   
        if x == 4:
            print("Histogramm vom ",a_string ,"-Sensor:", pick_column)
            hist = choosen_merged.hist(column=f"{save_string}")
        else:
            print("Die Eingabe ist ungültig!")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


# main

# # folgende Funktion dient zur Auswahl einer Tabelle aus der Datenbank
# pick_DataFrame()
# print("-----------------------------------------------------------------------------------------------------------------") 
# # soll den Bereich anzeigen in dem man ein Datum wählen kann
# startEnd_df()
# print("-----------------------------------------------------------------------------------------------------------------") 
# # folgenden Funktion dient dazu auszuwählen welchen Tag oder welchen Berreich Sie sich anschauen möchten
# choose_date(utc_stamp)

# # bestimmter Tag wurde ausgewählt
# if input_a == "1":
#     # da ein bestimmter Tag ausgewählt wurde muss die Zeit auf der X-Achse angezeigt werden
#     # Zeit aus dem DatFrame herausfiltern
#     df_date = filtered_df_date["longtime"].dt.date
#     # den ausgewählten tag abspeichern
#     df_date = df_date.iloc[0]
#     # den Tag als string abspeichern / für die angabe im plot
#     df_date = df_date.strftime("%m/%d/%Y")
# else:
#     pass

# # füge folgende DataFrames zusammen
# # pick_dataFrame() -> Temperatur- oder Luftfeuchtigkeitssensor
# # choose_date(utc_stamp) -> ausgewähltes Datum oder über ein längeren Zeitraum
# choosen_merged = pd.merge(filtered_df_date, pickd_column_df, left_index=True, right_index=True)    
    

# print("-----------------------------------------------------------------------------------------------------------------")    
# # zeige die größte Datenlücke in dem ausgewähltem DataFrame
# find_datagap(choosen_merged)
# print("-----------------------------------------------------------------------------------------------------------------") 


# # folgende Funktion gibt die Möglichkeiten einige statistische Verfahren auf eine ausgewählte Tabelle anzuwenden
# statistic_funcion_dynamic(choosen_merged, save_string)
# print("-----------------------------------------------------------------------------------------------------------------") 
# # folgende Funktion visualisiert die ausgewählten tabellen mit verschiedenene stat. Visualisierungen
# visual_method_dynamic(filtered_df_date, a, choosen_merged, input_a)
# #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#