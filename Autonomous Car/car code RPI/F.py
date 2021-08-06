#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)
reader = SimpleMFRC522()
import time
import pyrebase

def rfid():
    config = {
      "apiKey": "095e9c56792253d516853bb78544245dcca08f3d",
      "authDomain": "raspi-firebase-5cf35.firebaseapp.com",
      "databaseURL": "https://raspi-firebase-5cf35-default-rtdb.firebaseio.com",
      "storageBucket": "raspi-firebase-5cf35.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    print("Send Data to Firebase Using Raspberry Pi")
    print("----------------------------------------")
    try:
        for i in range(2):
            id, text = reader.read()
            print(id)
            data = {"rfid": id,}
            db.update(data)
            time.sleep(2)
           
    finally:
            GPIO.cleanup()
rfid()