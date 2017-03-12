#!/usr/bin/env python
# encoding: utf-8

__title__ = "Joystick"
__author__ = "Roboton Programing Team"
__version__ = ""

"""
    Joystick
    ~~~~~~~~~~~~~
    A program that read joystick input and send data to arduino using
    serial communication.
    w -> forward
    s -> backward
    a -> left
    d -> right
    n -> stop
    require:
        *python 2.7
        *pygame 1.9.1 library
        *pyserial 2.7 library
    :copyright: (c) 2015 by Roboton Programing Team
    Dalia Diab
    Mohab Adel
    Walid Yasir <waleedyaser95@gmail.com>
    Yasmin Elnezamy
"""
# importing libraries
import pygame
import serial

class JoystickControl(object):

    def __init__(self, ser):
        # init libraries
        pygame.init()
        pygame.joystick.init()

        self.ser = ser
        # check if joystick connceted
        if not pygame.joystick.get_count():
            print "\nPlease connect a joystick and run again.\n"
            quit()
        else :
            print "joysticks connceted:", pygame.joystick.get_count()

        #select joystick
        self.myjoy = pygame.joystick.Joystick(0)
        #init joystick
        self.myjoy.init()

    def joystick_read(self):
        """
            waiting for joystick events and handling it
        """
        print "init"
        while True:

            for event in pygame.event.get():

                # up button
                if self.myjoy.get_hat(0) ==  (0,1) :
                    print 'Forword'
                    self.ser.write('w')
                # down button
                elif self.myjoy.get_hat(0) == (0,-1):
                    print 'Backword'
                    self.ser.write('s')
                # left button
                elif self.myjoy.get_hat(0) == (-1,0) :
                    print 'Left'
                    self.ser.write('a')
                # right button
                elif self.myjoy.get_hat(0) == (1,0):
                    print 'Right'
                    self.ser.write('d')
                # x button
                elif self.myjoy.get_button(5):
                    print 'Stop !'
                    self.ser.write('n')
                elif self.myjoy.get_button(4):
                    print 'buzzer'
                    self.ser.write('z')
                elif self.myjoy.get_button(8):
                    print "close"
                    return 0
