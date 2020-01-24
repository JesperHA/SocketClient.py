#!/usr/bin/env python3

import socket
import time
import zlib

import numpy as np
import cv2
import pygame
import zmq
import base64
from multiprocessing import Process


HOST = ''  # The server's hostname or IP address
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
img = cv2.imread("airborne.jpg", 1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



s.bind((HOST, PORT))
s.listen()
print("Listening...")
conn, addr = s.accept()

print("Connected by: ", addr)


fps = 1
frames = 1

with conn:
    while True:

        startTime = time.time()


        # img = cv2.imread("airborne.jpg", 1)
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

        conn.sendall(bytes(value, 'utf8'))

        # time.sleep(0.00166)
        data = conn.recv(500000)
        # print("Data: ", data)
        try:
            img = None
            if data:
                # data = zlib.decompress(data)
                image_string = str(data, 'utf-8')
                # print("Image String: " + image_string)
                raw_image = base64.b64decode(image_string)
                print("Raw image")
                print(raw_image)

                image = np.frombuffer(raw_image, dtype=np.uint8)
                print("image: ", image)

                # print(image)
                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                # cv2.resizeWindow("image", 1280, 720)
                # cv2.resizeWindow("image", 720, 480)
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

s.close




