from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_redis import FlaskRedis
import eventlet
import os
from time import sleep

eventlet.monkey_patch()

mqtt = Mqtt( mqtt_logging=True)
socketio = SocketIO()
redisc = FlaskRedis()


GRID_HEIGHT = 3
GRID_WIDTH = 3

def create_app(debug=False):
    app = Flask(__name__)
    app.config['MQTT_BROKER_URL'] = os.getenv("MQTT_BROKER_URL")  
    app.config['MQTT_BROKER_PORT'] = int(os.getenv("MQTT_PORT"))
    app.config['MQTT_USERNAME'] = os.getenv("MQTT_USER")  
    app.config['MQTT_PASSWORD'] = os.getenv("MQTT_PASSWD")   
    app.config['MQTT_KEEPALIVE'] = 30  # set the time interval for sending a ping to the broker to 30 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
    app.config['MQTT_CLIENT_ID'] = os.getenv("MQTT_CLIENT_ID")

    app.config['REDIS_URL'] = os.getenv("REDIS_URL")
    app.debug = debug

    app.logger.debug("app config set")

    # register blueprints
    with app.app_context():
        app.logger.debug("registering blueprints...")
        from server.mqtt_func import mqtt_bp 
        from server.socketio_func import socketio_bp 
        from server.main import main_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(mqtt_bp)
        app.register_blueprint(socketio_bp)
        app.logger.debug("done registering!")


    # init mqtt and socketio
    app.logger.debug("initializing libraries...")
    mqtt.init_app(app)
    socketio.init_app(app)
    redisc.init_app(app)
    app.logger.debug("done initializing!")




    redisc.set('foo', 'bar')
    app.logger.debug(redisc.get('foo'))


    return app

# def create_subscribers(width, height):
#     for i in range(width*height):
#         topic = "{:03d}".format(i)
#         mqtt.subscribe(topic)

# @mqtt.on_connect()
# def mqtt_connect_cb(client, userdata, flags, rc):
#     print("bruh")
#     create_subscribers(GRID_WIDTH, GRID_HEIGHT)

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     print("sheesh")