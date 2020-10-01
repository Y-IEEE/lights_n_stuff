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

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    # mqtt.subscribe('To Photon')
    print("[CONNECTION]: MQTT Connected!")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)

def change_colors(chip_id, color):
    mqtt.publish(chip_id, color);

@app.route('/')
def base():
    # if "change_color" in request.form:
    #     mqtt.publish("To Chips", msg)
    return render_template('index.html')

@socketio.on("lights")
def change_lights_message(message):
    print("[LIGHTS] : " + str(message))
    emit(message, json=True)
    change_colors(message["id"], message["color"])

@socketio.on("info")
def print_debug(message):
    print("[INFO]: " + str(message))

@socketio.on("connect")
def on_connect():
    print("[CONNECTION]: Socket connected!")



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')