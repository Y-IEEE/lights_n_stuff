from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import os


mqtt = Mqtt()
socketio = SocketIO()

GRID_HEIGHT = 3
GRID_WIDTH = 3

def create_app(debug=False):
    app = Flask(__name__)
    app.config['MQTT_BROKER_URL'] = os.getenv("MQTT_BROKER_URL")  
    app.config['MQTT_BROKER_PORT'] = int(os.getenv("MQTT_PORT"))
    app.config['MQTT_USERNAME'] = os.getenv("MQTT_USER")  
    app.config['MQTT_PASSWORD'] = os.getenv("MQTT_PASSWD")   
    app.config['MQTT_KEEPALIVE'] = 10  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
    app.debug = debug

    # init mqtt and socketio
    mqtt.init_app(app)
    socketio.init_app(app)

    # register blueprints
    with app.app_context():
        from server import mqtt_func, socketio_func, main
        app.register_blueprint(main.bp)
        app.register_blueprint(mqtt_func.bp)
        app.register_blueprint(socketio_func.bp)

    return app