#!/usr/bin/env python3

import socket
import time
import numpy as np
import cv2
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

servoRange = 500
throttle = 0
stringXAxis = "xAxis "
stringYAxis = "yAxis "
stringZAxis = "zAxis "
value = " "
font = cv2.FONT_HERSHEY_PLAIN

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))



    while True:

        img = cv2.imread("airborne.jpg", 1)
        # value = input("Input new value: ")
        pygame.event.pump()

        xInput = joystick.get_axis(0) * servoRange
        yInput = joystick.get_axis(1) * servoRange
        zInput = joystick.get_axis(3) * servoRange

        throttle = joystick.get_axis(2)
        throttle = (((throttle + 1) * 50) - 100) * -1

        if joystick.get_button(1) == 1:
            value = "q"

        if joystick.get_button(1) != 1:
            xData = str(xInput + 1500)
            yData = str(yInput + 1500)
            zData = str(zInput + 1500)
            tData = str(500 + (throttle * 20))
            value = ("control " + xData + " " + yData + " " + zData + " " + tData)

        s.sendall(bytes(value, 'utf8'))

        # time.sleep(0.00166)

        data = s.recv(1024)

        string = "Throttle: " + str(int(throttle)) + "%"

        cv2.rectangle(img, (100, 200), (150 + 80, 200 + 25), (255, 255, 255), 1)
        cv2.putText(img, string, (101, 218), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("image", img)




