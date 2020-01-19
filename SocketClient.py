#!/usr/bin/env python3

import socket
import time

import pygame


HOST = '192.168.7.238'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("Joystick recognized: ")
print(joystick.get_name())
print(joystick.get_numbuttons())


stringXAxis = "xAxis "
stringYAxis = "yAxis "
stringZAxis = "zAxis "
value = " "
xAxis = 500

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))

    while True:
        # value = input("Input new value: ")
        pygame.event.pump()
        joystick.get_axis(0)
        joystick.get_axis(1)
        joystick.get_axis(2)
        joystick.get_axis(3)

        xInput = joystick.get_axis(0) * 1000
        yInput = joystick.get_axis(1) * 1000
        zInput = joystick.get_axis(3) * 1000



        if joystick.get_button(1) == 1:
            value = "q"

        if joystick.get_button(1) != 1:
            xData = str(xInput + 1500)
            yData = str(yInput + 1500)
            zData = str(zInput + 1500)
            value = (stringXAxis + xData + " " + stringYAxis + yData + " " + stringZAxis + zData)

        # if xInput < 0:
        #     data = str(xInput + 1500)
        #     value = (string + data)>



        s.sendall(bytes(value, 'utf8'))

        time.sleep(1)


        # data = s.recv(1024)

        # print('Received', repr(data))