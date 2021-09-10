

string = "allees_KLAR_BEI DIR_0 oder doch die 12"


# folgende Funktion dient zum filtern der Nummer des Strings
SensNumber= [int(s) for s in string.split() if s.isdigit()]
for i in SensNumber:
    if i >0:
        save_number_string = str(i)


print(save_number_string)