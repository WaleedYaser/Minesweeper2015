#!/usr/bin/env python
# encoding: utf-8

__title__ = "Main code"
__author__ = "Roboton Programing Team"
__version__ = ""

"""
    Main code
    ~~~~~~~~~~~~~
    the main code of our software ...
    require:
        *python 2.7
        *pyserial 2.7 library
        *pygame 1.9.1 library
        *joystick.py
        *encoder.py
        *gui.py
    :copyright: (c) 2015 by Roboton Programing Team 
    Dalia Diab
    Mohab Adel
    Walid Yasir <waleedyaser95@gmail.com>
    Yasmin Elnezamy
"""

# importing libraries
from Gui import GUI
from Tkinter import Tk
import time
import datetime


# main function
def main():
    # root window
    root = Tk()
    now = datetime.datetime.now()
    #filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename1 = "data/mine"
    f = open(filename1 + ".txt", "w")
    # object of GUI class
    app = GUI(root, f)


    # main loop for gui
    root.mainloop()
    f.close()


if __name__ == "__main__":
    main()
