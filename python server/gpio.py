# Python backend for RPI GPIO Controller Application
# Written by Johan Berglind

import socket
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
LED = 4
GPIO.setup(LED, GPIO.OUT)


# Leave this empty if you don't want it to bind to something specific
HOST = ''
PORT = 2323
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")
s.bind((HOST, PORT))
print("Socket bound")
s.listen(1)
# Initial GPIO mode
z = 0
GPIO.output(LED, GPIO.LOW)

while True:
    connection, ip = s.accept()
    print 'Connection from:', ip
    data = connection.recv(1024)
    # The Android application sends a string in UTF8 format, the following line is to decode it.
    data = data.decode("utf-8")
    if not data:
       break
    if 'on' in data:
        print("LIGHTS ON!")
        GPIO.output(LED, GPIO.HIGH)
        z = 1
        connection.close()
    elif 'off' in data:
        print("LIGHTS OFF!")
        GPIO.output(LED, GPIO.LOW)
        z = 0
        connection.close()
    elif 'status' in data:
        print("Status command detected")
        if z == 0:
            connection.send('off')
            print("Sent off response")
            connection.close()
        else:
            connection.send('on')
            print("Sent on response!")
            connection.close()
    else:
        print('Wrong command! The command sent:{}'.format(data))

