import pygame
import paho.mqtt.client as mqtt

def on_connect(mqttc, obj, flags, rc):
    print("connected: " + str(rc))

def on_message(mqttc, obj, msg):
    global gotSize, xSize, ySize
    #get the size of the array being sent
    if (msg.topic == "size"):
        print("PAYLOAD SIZE: ", msg.payload)

        xNum = int(str(msg.payload)[2:4])
        yNum = int(str(msg.payload)[5:7])
        #go through and subscribe to all necessary commands
        for x in range(xNum):
            for y in range(yNum):
                IDString = str(x).zfill(2) + "x" + str(y).zfill(2)
                #print(IDString)
                mqttc.subscribe(IDString)
        #set the size of each rectangle
        xSize = int(width / xNum)
        ySize = int(height / yNum)
        #print("width: " + str(xSize) + " height: "+ str(ySize))
        gotSize = True
    else:  #when you get a command
        print("PAYLOAD CMD: ", msg.payload)
        xID = int(str(msg.topic)[0:2])  
        yID = int(str(msg.topic)[3:5])
        #set rectangle at correct location to color in payload
        tempRect = pygame.Rect((xSize*xID), (ySize*yID), xSize, ySize)
        tempColor = "#" + str(msg.payload)[2:8]
        pygame.draw.rect(screen, pygame.Color(tempColor), tempRect)
        pygame.display.flip()
        


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

#set screen width and height
width = 1000
height = 800
#set up screen
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))
gotSize = False
#set up mqtt & subscribe to size - then loop forever
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.username_pw_set("yale", "lightsnstuff")
mqttc.connect("35.239.98.209", 14479)
mqttc.subscribe("size")
mqttc.loop_forever()
        
