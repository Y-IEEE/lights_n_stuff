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
size = [int(x) for x in file.readline().split('x')]
xSize = size[0]
ySize = size[1]
print("x:", xSize, "y:", ySize)

fps = int(file.readline())
print("fps:", fps)

isEOF = True

while True:
    start_pos = file.tell()
    line = file.readline()
    # print('starting with: ', line)

    # skip all the beginning stuff
    while (isEOF and '---' not in line):
        # print('skipping: ', line)
        start_pos = file.tell()
        line = file.readline()
    isEOF = False

    # find the next frame
    while (line == '\n' or '---' in line):
        start_pos = file.tell()
        line = file.readline()

    # check if EOF
    if line == '':
        print("EOF")
        file.seek(0, os.SEEK_SET)
        isEOF = True
        continue

    # if it has reached here, we are now reading a valid frame

    # unread the first line of frame
    file.seek(start_pos, os.SEEK_SET)

    for y in range (0, ySize):
        wholeLine = file.readline()
        print(wholeLine)

        lineWords = wholeLine.split()
        for x in range(0, xSize):
            pixel = str(x).rjust(2, '0') + "x" + str(y).rjust(2, '0')
            # print("line: ", lineWords)
            # pixel = "{:03d}".format(i)
            print("id:", pixel, "command:", lineWords[x])
            
            optionalTag = '#' if lineWords[x][0] != '#' else ''
            mqttc.publish(pixel, optionalTag + lineWords[x])

    time.sleep(1/fps)

file.close()