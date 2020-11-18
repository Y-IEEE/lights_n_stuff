from server import mqtt
# from flask import current_app as app
from server import socketio

def change_colors(chip_id, color):
    mqtt.publish(str(chip_id), color)

def update_clients(light_id, val):
    app.logger.debug("Updating clients...: ({}, {})".format(light_id, val))
    message = {"id": light_id, "color": val}
    socketio.emit("server_update_light", message, json=True) # broadcast=true not needed for socketio.emit
    