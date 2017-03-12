#!/usr/bin/env python
# encoding: utf-8

__title__ = "Main Gui"
__author__ = "Roboton Programing Team"
__version__ = ""

"""
    Main Gui
    ~~~~~~~~~~~~~
    A program that create our Gui and map.
    require:
        *python 2.7
"""

# importing libraries
from Tkinter import *
import serial
import thread

from Joystick import JoystickControl
from enc import Encoder

from tkFileDialog import askopenfilename

class GUI(object, Frame):

    # check mines variables
    x_old = 0
    y_old = 0
    flag = True

    def __init__(self, parent, sheet):
        # init frame
        Frame.__init__(self, parent)

        self.parent = parent
        self.sheet = sheet
        self.buildGui()

    def buildGui(self):
        """
            build components of gui and show it
        """

        # set title and make frame fill window
        self.parent.title("where 's my mine")
        self.pack(fill = BOTH, expand = 1)



        # init map grids
        for i in range(0,19):
            self.columnconfigure(i, pad = 5)
            self.rowconfigure(i, pad = 5)

        #init tools grid
        for i in range(19, 23):
            self.columnconfigure(i, pad = 10)
            self.rowconfigure(i, pad = 10)

        self.buttons = []       # buttons array for map

        # fill array with 19 column and 19 row
        for i in range(19):
            self.buttons.append([])
            for j in range(19):
                t =  i + 1,":" , j + 1
                self.buttons[i].append(Button(self, text = t, width = 4, height = 1))
                self.buttons[i][j].grid(row = 18 - i + 1, column = 18 - j)
                self.buttons[i][j]["bg"] = "white" # color white


        # entry comm_num
        Label(self, text = "COM number : ", fg = "blue").grid(row = 2 , column = 19)
        self.e1=Entry(self, fg = "dark grey")
        self.e1.grid(row=2,column=20)

        self.e1.insert(0, "COM10")


        Button(self,text='connect serial',command=self.connect_serial).grid(row=2,column=22)

        self.serial_connected = Label(self, text = "not connected", fg = "red")
        self.serial_connected.grid(row = 2, column = 21)

        # entry manual draw
        Label(self, text = "Manual plot : ", fg = "blue").grid(row = 8, column = 19)
        self.e2=Entry(self)
        self.e2.grid(row=8,column=20)



        Button(self,text='Manual Draw',command=self.manual_draw).grid(row=8,column=21)
        Button(self,text="Import",command=self.import_file).grid(row=8,column=22)

        # connect serial button
        Label(self, text = "Joystick : ", fg = "blue").grid(row = 4, column = 19)
        Label(self, text = "Arduino : ", fg = "blue").grid(row = 4, column = 21)

        self.joy_button = Button(self,text='connect joystick',state=DISABLED ,command=self.connect_joystick)
        self.joy_button.grid(row=5,column=20)
        self.joystick_connected = Label(self, text = "not connected", fg = "red")
        self.joystick_connected.grid(row = 5, column = 19)

        self.read_button = Button(self,text='Read serial', state=DISABLED, command=self.connect_arduino)
        self.read_button.grid(row=5,column=22)
        self.read_serial = Label(self, text = "not recieving", fg = "red")
        self.read_serial.grid(row = 5, column = 21)

        # Labels #####################
        # recieved message label
        Label(self, text = "recieved message : ", fg = "blue").grid(row = 11, column = 19)
        self.message = StringVar()
        self.message.set("None")
        Label(self, textvariable = self.message).grid(row = 11, column = 20)

        # left ticks label
        Label(self, text = "Left ticks : ", fg = "blue").grid(row = 13, column = 19)
        self.left_tick = StringVar()
        self.left_tick.set("None")
        Label(self, textvariable = self.left_tick).grid(row = 13, column = 20)

        # Right ticks Label
        Label(self, text = "Right ticks : ", fg = "blue").grid(row = 13, column = 21)
        self.right_tick = StringVar()
        self.right_tick.set("None")
        Label(self, textvariable = self.right_tick).grid(row = 13, column = 22)

        # distance x axis
        Label(self, text = "X distance : ", fg = "blue").grid(row = 15, column = 19)
        self.x_distance= StringVar()
        self.x_distance.set("None")
        Label(self, textvariable = self.x_distance).grid(row = 15, column = 20)

        Label(self, text = "Y distance : ", fg = "blue").grid(row = 15, column = 21)
        self.y_distance = StringVar()
        self.y_distance.set("None")
        Label(self, textvariable = self.y_distance).grid(row = 15, column = 22)

        Label(self, text = "Theta : ", fg = "blue").grid(row = 16, column = 19)
        self.theta = StringVar()
        self.theta.set("None")
        Label(self, textvariable = self.theta).grid(row = 16, column = 20)

        Label(self, text = "Current square : ", fg = "blue").grid(row = 18, column = 19)
        self.square = StringVar()
        self.square.set("None")
        Label(self, textvariable = self.square).grid(row = 18, column = 20)

        ###########################

        self.mine_alarm = Label(self ,bg = "yellow")
        self.mine_alarm.grid(row = 17, column = 22, columnspan = 1,
                             rowspan = 2 , sticky = N + S + E + W, padx = 10)

        self.pack()

    #function to import file
    def import_file(self):
        f = askopenfilename()
        my_file=open(f,"r")

        for i in my_file:
           self.get_position(i)


    def get_position(self,line):

        read_line=line.split(":")
        x=int(read_line[0])
        y=int(read_line[1])
        m=int(read_line[2])
        self.draw_mine(x,y,m)

    # connect serial button handler
    def connect_arduino(self):
        self.enc = Encoder(self, self.arduino)
        thread.start_new_thread(self.enc.read_serial, (self.sheet, ))
        self.read_serial["text"] = "connected"
        self.read_serial["fg"] = "dark green"


    def connect_joystick(self):
        self.joy = JoystickControl(self.arduino)
        thread.start_new_thread(self.joy.joystick_read, ())
        self.joystick_connected["text"] = "connected"
        self.joystick_connected["fg"] = "dark green"

    def manual_draw(self):
        map=self.e2.get().split(":")
        x=int(map[0])
        y=int(map[1])
        mine_state=int(map[2])
        self.draw_mine(x,y,mine_state)

    def connect_serial(self):

      	"""
      			connect serial
        """


        # handle serial connection error
        try:

            com_num=self.e1.get()
            self.arduino=serial.Serial(com_num,9600)
            self.serial_connected["text"] = "connected (" + com_num + ")"
            self.serial_connected["fg"] = "dark green"
            self.joy_button["state"] = NORMAL
            self.read_button["state"] = NORMAL

        except IOError as e :
            print "Serial Communication Cannot Establish (Please Check your Comnum) ",e
            self.serial_connected["text"] = "not connected"
            self.serial_connected["fg"] = "red"
            self.joy_button["state"] = DISABLED
            self.read_button["state"] = DISABLED

    def draw_mine(self, x, y, m):
        """
            plot mines on map grid
        """

        # check state
        x_change = (x != self.x_old)
        y_change = (y != self.y_old)
        if x_change or y_change:
            self.flag= True

        # plot state
        if m == 2:
            self.buttons[x][y]["bg"] = "red"
            #self.update()

        elif m == 1:
            self.buttons[x][y]["bg"] = "blue"
            #self.update()


        elif m == 0 and self.flag:
            self.flag = False
            self.buttons[x][y]["bg"] = "green"
            #self.update()


        self.x_old = x
        self.y_old = y
