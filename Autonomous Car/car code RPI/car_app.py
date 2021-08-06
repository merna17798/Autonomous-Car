import F
from socket import *
from time import ctime
import RPi.GPIO as GPIO
import time
# Servomotor.setup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)  # motor 2
GPIO.setup(6, GPIO.OUT)  # motor 2
GPIO.setup(13, GPIO.OUT)  # motor 1
GPIO.setup(19, GPIO.OUT)  # motor 1
ctrCmd = [b'forward',b'backward',b'right',b'left',b'server',b'embeded']

HOST = '172.28.128.189'
PORT = 4000


BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

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
    time.sleep(0.2)
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
    time.sleep(0.2)
    print('x')
    GPIO.output(5, False)
    GPIO.output(6, False)
    GPIO.output(13, False)
    GPIO.output(19, False)
while True:
        print ('Waiting for connection')
        tcpCliSock,addr = tcpSerSock.accept()
        print ('...connected from :', addr)
        try:
                while True:
                        data = ''
                        data = tcpCliSock.recv(BUFSIZE)
                        print(data)
                        if not data:
                                break
                        if data == ctrCmd[0]:
                            forward()                          
                            print ('forward')

                        if data == ctrCmd[2]:
                            right()
                            data = ''
                            print ('right')
                        if data == ctrCmd[3]:
                            left()
                            data = ''
                            print ('left')                            
        except KeyboardInterrupt:
                GPIO.cleanup()
tcpSerSock.close();