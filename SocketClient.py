#!/usr/bin/env python3

import socket
import time
import numpy as np
import cv2
import pygame
import base64
from multiprocessing import Process


HOST = ''  # The server's hostname or IP address
PORT = 65432       # The port used by the server
server_address = (HOST, PORT)
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
img = cv2.imread("airborne.jpg", 1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



s.bind(server_address)
# s.listen()
print("Listening...")
# conn, addr = s.accept()
#
# print("Connected by: ", addr)


fps = 1
frames = 1

# with conn:
while True:
    startTime = time.time()
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

    data, address = s.recvfrom(50000)
    s.sendto(bytes(value, 'utf8'), address)
    try:
        print("Data: ", data)
        dataString = str(data, 'utf-8')
        print("bytes data conversion succesful")
        dataStrings = dataString.split()
        print("data split succesful")

        if dataStrings[0] == "image":
            print("Entered if statement")
        # if data:
            try:
                img = None
                if data:

                    raw_image = base64.b64decode(dataStrings[1])
                    image = np.frombuffer(raw_image, dtype=np.uint8)
                    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                    # cv2.resizeWindow("image", 1280, 720)
                    img = cv2.imdecode(image, 1)
                    data = None
                string = "Throttle: " + str(int(throttle)) + "%"
                cv2.rectangle(img, (100, 200), (150 + 80, 200 + 25), (255, 255, 255), 1)
                cv2.putText(img, string, (101, 218), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imshow("image", img)
            except:
                print("Didn't work")

            delay = time.time() - startTime
            # sleep = ((1 / 24) - delay % (1 / 24))
            # time.sleep(sleep)
            tickTime = delay
            tickrate = 1 / tickTime

            frames += 1
            fps += tickrate
            realFps = fps / frames

            # print("tickTime: ", tickTime)
            # print("tickrate: ", tickrate)
            print("fps: ", realFps)
    except:
        print("No image data")
# s.close




