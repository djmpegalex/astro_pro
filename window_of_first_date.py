import tkinter
import math

from constants import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *

def get_window_of_first_date():
    """
        Create new window
    """
    window_of_first_date = tkinter.Tk()
    window_of_first_date.title("edition date data")
    window_of_first_date.geometry('300x150+650+0')

    window_of_first_date.mainloop()
