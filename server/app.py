import eventlet
import json
from flask import Flask, render_template, redirect, url_for
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_redis import FlaskRedis
import os
# from flask_bootstrap import Bootstrap

# CONSTANTS
GRID_HEIGHT = 3
GRID_WIDTH = 3

eventlet.monkey_patch()

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = os.getenv("MQTT_BROKER_URL")  
app.config['MQTT_BROKER_PORT'] = int(os.getenv("MQTT_PORT"))
app.config['MQTT_USERNAME'] = os.getenv("MQTT_USER")  
app.config['MQTT_PASSWORD'] = os.getenv("MQTT_PASSWD")   
app.config['MQTT_KEEPALIVE'] = 30  # set the time interval for sending a ping to the broker to 30 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['MQTT_CLIENT_ID'] = os.getenv("MQTT_CLIENT_ID")

app.config['REDIS_URL'] = os.getenv("REDIS_URL")
app.debug = os.getenv("DEBUG")

mqtt = Mqtt(app)
socketio = SocketIO(app)
redisc = FlaskRedis(app, charset="utf-8", decode_responses=True)

# initalize some starting stuff
redisc.set('clients', 0)

'''             
*********************
    FLASK ROUTES 
*********************
'''

@app.route('/')
def base():
    return redirect(url_for('grid_page'))

@app.route('/grid')
def grid_page():
    return render_template('index.html')



'''             
*********************
  UTILITY FUNCTIONS
*********************
'''

def change_colors(chip_id, color):
    mqtt.publish(str(chip_id), color)

def update_clients(light_id, val):
    app.logger.debug("Updating clients...: ({}, {})".format(light_id, val))
    message = {"id": light_id, "color": val}
    socketio.emit("server_update_light", message, json=True) # broadcast=true not needed for socketio.emit



'''             
******************
SOCKETIO FUNCTIONS
******************
'''

# receive light change command from client
@socketio.on("client_update_light")
def change_lights_message(message):
    app.logger.debug("Change Lights: " + str(message))

    # change colors on MQTT
    change_colors(message["id"], message["color"])

    # update internal light array, id = index which is really bad rn, find a better way of doing this
    # grid_list[int(message['id'])].set_color(message['color'])
    update_clients(message['id'], message['color'])   

# debug channel
@socketio.on("info")
def print_debug(message):
    app.logger.debug("Client Debug: " + str(message))

# when client connects to site
@socketio.on("connect")
def on_connect():
    redisc.incr('clients')
    app.logger.debug("Socket connected! Currently connected clients: {}".format(redisc.get('clients')))
    # for light in grid_list:
    #     print(light)

    # # send the newly connected client the current color statuses
    # for node in grid_list:
    #     update_clients(node.get_id(), node.get_color())

@socketio.on("disconnect")
def on_disconnect():
    redisc.decr('clients')
    app.logger.debug("Client disconnected! Currently connected clients: {}".format(redisc.get('clients')))


'''             
******************
  MQTT FUNCTIONS
******************
'''


def create_subscribers(width, height):
    for i in range(width*height):
        topic = "{:03d}".format(i)
        mqtt.subscribe(topic)

@mqtt.on_connect()
def mqtt_connect_cb(client, userdata, flags, rc):
    app.logger.debug("MQTT Connected!")
    create_subscribers(GRID_WIDTH, GRID_HEIGHT)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    app.logger.debug("Received message! [{}]: {}".format(message.topic, message.payload.decode()))
    update_clients(message.topic, message.payload.decode())

if __name__ == '__main__':
    socketio.run(app, port=os.getenv("PORT"), host='0.0.0.0', use_reloader=False)