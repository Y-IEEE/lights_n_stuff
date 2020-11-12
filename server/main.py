from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
import time
import os

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = os.getenv("MQTT_BROKER_URL")  
app.config['MQTT_BROKER_PORT'] = int(os.getenv("MQTT_PORT"))
app.config['MQTT_USERNAME'] = os.getenv("MQTT_USER")  
app.config['MQTT_PASSWORD'] = os.getenv("MQTT_PASSWD")   
app.config['MQTT_KEEPALIVE'] = 10  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)
socketio = SocketIO(app)

class LightNode:
    def __init__(self, id):
        self._id = id
        self._color = "#ffffff"

    def get_id(self):
        return self._id

    def get_color(self):
        return self._color

    def set_color(self, newCol):
        self._color = newCol

    def __str__(self):
        return "[{}]: {}".format(self._id, self._color)

grid_list = []
num_clients = 0

def set_up_grid(width, height):
    global grid_list
    grid_list = [LightNode(i) for i in range(width*height)]
    for grid in grid_list:
        print(grid)

def update_clients(light_id, val):
    print("Updating clients...: ({}, {})".format(light_id, val))
    message = {"id": light_id, "color": val}
    emit("server_update_light", message, json=True, broadcast=True)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    # mqtt.subscribe('To Photon')
    print("[CONNECTION]: MQTT Connected!")
    mqtt.subscribe("001")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("Received message!" + message.payload.decode())
    update_clients("1", message.payload.decode())

def change_colors(chip_id, color):
    mqtt.publish(str(chip_id), color)

# receive light change command from client
@socketio.on("client_update_light")
def change_lights_message(message):
    global grid_list
    print("[LIGHTS] : " + str(message))
    # emit("lights", message, json=True, broadcast=True)

    # change colors on MQTT
    change_colors(message["id"], message["color"])

    # update internal light array, id = index which is really bad rn, find a better way of doing this
    grid_list[int(message['id'])].set_color(message['color'])
    update_clients(message['id'], message['color'])

    

# debug channel
@socketio.on("info")
def print_debug(message):
    print("[INFO]: " + str(message))

# when client connects to site
@socketio.on("connect")
def on_connect():
    global num_clients
    num_clients += 1
    print("[CONNECTION]: Socket connected! Active Clients = {}".format(num_clients))
    for light in grid_list:
        print(light)

    # send the newly connected client the current color statuses
    for node in grid_list:
        update_clients(node.get_id(), node.get_color())

@socketio.on("disconnect")
def on_disconnect():
    global num_clients
    num_clients -= 1
    print("[DISCONNECTION]: Client disconnected! Active Clients = {}".format(num_clients))

@app.route('/')
def base():
    return render_template('index.html')


if __name__ == '__main__':
    set_up_grid(3, 3)
    socketio.run(app, host='0.0.0.0')