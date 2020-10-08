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

grid_list = []

def set_up_grid(width, height):
    global grid_list
    grid_list = [LightNode(i) for i in range(width*height)]

def update_light(light_id, val):
    message = {"id": light_id, "color": val}
    emit("server_update_light", message, json=True, broadcast=True)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    # mqtt.subscribe('To Photon')
    print("[CONNECTION]: MQTT Connected!")

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     data = dict(
#         topic=message.topic,
#         payload=message.payload.decode()
#     )
#     print(data)

def change_colors(chip_id, color):
    mqtt.publish(chip_id, color)

# receive light change command from client
@socketio.on("client_update_light")
def change_lights_message(message):
    print("[LIGHTS] : " + str(message))
    # emit("lights", message, json=True, broadcast=True)

    # change colors on MQTT
    change_colors(message["id"], message["color"])

    # update internal light array, id = index which is really bad rn, find a better way of doing this
    grid_list[int(message['id'])].set_color(message['color'])

    

# debug channel
@socketio.on("info")
def print_debug(message):
    print("[INFO]: " + str(message))

# when client connects to site
@socketio.on("connect")
def on_connect():
    print("[CONNECTION]: Socket connected!")

    # send the newly connected client the current color statuses
    for node in grid_list:
        update_light(node.get_id(), node.get_color())


@app.route('/')
def base():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    set_up_grid(3, 3)