#!/usr/bin/env python
# encoding: utf-8

__title__ = "Encoder"
__author__ = "Roboton Programing Team"
__version__ = ""

"""
    Encoder
    ~~~~~~~~~~~~~
    A program that read left, right encoder tick and metal detector
    state, proccess data and output x, y plot state on the map .
    x, y between 0 and 19
    state = 0 : no mine
    state = 1 : mine above
    state = 2 : mine below
    require:
        *python 2.7
        *pyserial 2.7 library
    :copyright: (c) 2015 by Roboton Programing Team
    Dalia Diab
    Mohab Adel
    Walid Yasir <waleedyaser95@gmail.com>
    Yasmin Elnezamy
"""

# importing libraries
import serial
from math import pi,sin,cos,atan2

class Encoder(object):
    # Encoder Attributes
    R = 6     #radius of the robot free wheel
    L = 44   #the distance between the two free wheel
    N = 16    #encoders' ticks per revolution

    theta = 0      #angle of robot
    x = 0          #x position of robot
    y = 50          #y position of robot
    ticks_l_old = 0    # old ticks of left encoder
    ticks_r_old = 0    # old ticks of right encoder

    def __init__(self, app, ser):
        self.app = app

        #serial init
        self.ser = ser

    def get_xy(self, ticks_l, ticks_r):
        """
        this method apply these equations to return x and y
            * find delta ticks
            * find distance : 2 pi R delta_ticks / N
            * find Dc -distance center- : (distance_right + distance_left) / 2
            * find x_new : x_old + Dc cos(theta)
            * find y_new : y_old + Dc sin(theta)
            * find theta_new : theta_old + (Dr - Dl) / l
            * correct theta: atan2(sin(theta), cos(theta))
        """
        # find delta ticks
        delta_ticks_l = ticks_l - self.ticks_l_old
        delta_ticks_r = ticks_r - self.ticks_r_old

        # ubdate old ticks
        self.ticks_l_old = ticks_l
        self.ticks_r_old = ticks_r

        # find distance
        dl = 2 * pi * self.R * delta_ticks_l / self.N
        dr = 2 * pi * self.R * delta_ticks_r / self.N
        dc = (dr + dl) / 2

        # find x, y
        self.x = round(self.x + dc * cos(self.theta), 3)
        self.y = round(self.y + dc * sin(self.theta), 3)


        # find theta
        self.theta += (dr - dl) / self.L
        self.theta = atan2(sin(self.theta), cos(self.theta))

        # return
        return self.x, self.y, round(self.theta * 180 / pi, 3)

    def read_serial(self, sheet):
        """
            while loop to read serial data from arduino
            data in the form "left tick:right tick:state"
            analyse data and plot mines
        """

        while True:
            # read serial

            mes = self.ser.readline()

            self.app.message.set(mes[:-2])

            # split data
            mes = mes.split(":")
            print mes
            try:
                left = int(mes[0])
                self.app.left_tick.set(left)

                right = int(mes[1])
                self.app.right_tick.set(right)

                state = int(mes[2])
                self.alarm(state)

                # get x and y
                x_y =  self.get_xy(left, right)
                self.app.x_distance.set(x_y[0])
                self.app.y_distance.set(x_y[1])
                self.app.theta.set(x_y[2])


                # plot
                x = int(x_y[0] / 100)   # x square's number

                y = int(x_y[1] / 100)   # y square's number

                self.app.draw_mine(x, y, state)

                self.app.square.set(str(x) + " : " +  str(y))

                sheet.write(str(x) + ":" + str(y) + ":" + str(state)+"\n")

            except :
                print "error"
                return 1

    def alarm(self, state):
        if state == 1:
            self.app.mine_alarm["bg"] = "blue"
        elif state == 2:
            self.app.mine_alarm["bg"] = "red"
        elif state == 0:
            self.app.mine_alarm["bg"] = "green"
        else:
            self.app.mine_alarm["bg"] = "yellow"
