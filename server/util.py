from server import mqtt, socketio, redisc
import logging

log = logging.getLogger('server.util')

def change_colors(chip_id, color):
    log.info("Sending MQTT message: {{topic: {}, message: {} }}".format(chip_id, color))
    mqtt.publish(str(chip_id), color)

def update_clients(light_id, val):
    log.info("Updating clients...: ({}, {})".format(light_id, val))
    message = {"id": light_id, "color": val}
    redisc.set(int(light_id), val)
    socketio.emit("server_update_light", message, json=True) # broadcast=true not needed for socketio.emit
    
def create_subscribers(width, height):
    for i in range(width*height):
        topic = "{:03d}".format(i)
        log.info("Subscribing to Topic: {}".format(topic))
        mqtt.subscribe(topic)

# sets grid to white and re-creates subscribers
def reset_grid(width, height):
    for i in range(width*height):
        # subscribe to appropriate mqtt topic
        topic = "{:03d}".format(i)
        log.info("Subscribing to Topic: {}".format(topic))
        mqtt.subscribe(topic)

        # populate the board with white tiles
        message = {"id": i, "color": "#ffffff"}
        redisc.set(i, "#ffffff")
        socketio.emit("server_update_light", message)