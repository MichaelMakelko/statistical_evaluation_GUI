import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

# --- functions ---
def new_funcion():
    print("you are in new funcion")



def newselection(event):
    print('selected:', event.widget.get())
    compare = event.widget.get()

    if compare == "a":
        new_funcion()

# --- main ---


root = tk.Tk()

cb1 = ttk.Combobox(root, values=('a', 'c', 'g', 't'))
cb1.pack()
cb1.bind("<<ComboboxSelected>>", newselection)

cb2 = ttk.Combobox(root, values=('X', 'Y', 'XX', 'XY'))
cb2.pack()
cb2.bind("<<ComboboxSelected>>", newselection)

root.mainloop()


