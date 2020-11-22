#!/usr/bin/env python3

#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import os
import time


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(obj))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client("publish_animations")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.username_pw_set("yale", "lightsnstuff")
mqttc.connect("35.239.98.209", 14479)

fileName = input("Enter text file name: ")
file = open(fileName, "r")
size = file.readline()
xSize = int(size[0:2])
ySize = int(size[3:5])
print("x:", xSize, "y:", ySize)

mqttc.publish("size", size[0:5])

fps = int(file.readline())
print("fps:", fps)

while True:
    blankLine = file.readline()
    i = 0
    for y in range (0, ySize):
        wholeLine = file.readline()
        if wholeLine == '':
            print("EOF")
            mqttc.publish("size", size[0:5])
            file.seek(13, os.SEEK_SET) # 12 for single digit fps
            wholeLine = file.readline()
        lineWords = wholeLine.split()
        for x in range(0, xSize):
            pixel = str(x).rjust(2, '0') + "x" + str(y).rjust(2, '0')
            # pixel = "{:03d}".format(i)
            print("id:", pixel, "command:", lineWords[x])
            mqttc.publish(pixel, "#" + lineWords[x])
            i += 1

    time.sleep(1/fps)




file.close()