import time
import picamera
import socket
import pickle
import cv2
import numpy as np
import RPi.GPIO as GPIO
import base64
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)  # motor 2
GPIO.setup(6, GPIO.OUT)  # motor 2
GPIO.setup(13, GPIO.OUT)  # motor 1
GPIO.setup(19, GPIO.OUT)  # motor 1
TRIG=23
ECHO=24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
def forward():
    GPIO.output(5, False)
    GPIO.output(6, True)
    GPIO.output(13, False)
    GPIO.output(19, True)
    time.sleep(0.3)
    print('x')
    GPIO.output(5, False)
    GPIO.output(6, False)
    GPIO.output(13, False)
    GPIO.output(19, False)

def left():
    GPIO.output(5, False)
    GPIO.output(6, True)
    GPIO.output(13, False)
    GPIO.output(19, False)
    time.sleep(0.3)
    print('x')
    GPIO.output(5, False)
    GPIO.output(6, False)
    GPIO.output(13, False)
    GPIO.output(19, False)
def right():
    GPIO.output(5, False)
    GPIO.output(6, False)
    GPIO.output(13, False)
    GPIO.output(19, True)
    time.sleep(0.3)
    print('x')
    GPIO.output(5, False)
    GPIO.output(6, False)
    GPIO.output(13, False)
    GPIO.output(19, False)
while True:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 1
        time.sleep(1.5)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output,'rgb')
        imgGray = cv2.cvtColor(output,cv2.COLOR_RGB2GRAY)
        print (imgGray)
        msg =pickle.dumps(imgGray)
        a_file = open("test.txt", "wb")
        a_file.write(msg)
        a_file.close()
        fo=open("test.txt" ,"rb")
        g=fo.read()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('172.28.128.183', 8800))
        data_length = len(g)
        client.send(data_length.to_bytes(4, 'big'))
        client.send(g)
        print('sent')
        from_server = client.recv(4096)
        client.close()
        from_server=from_server.decode("utf-8")
        print (from_server)
        if from_server == 'F':
            forward()
            
        if from_server == 'R':
            right()
            
        if from_server == 'L':
            left()
