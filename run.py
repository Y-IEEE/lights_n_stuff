from server import create_app, socketio
import os

app = create_app()

if __name__ == '__main__':
    socketio.run(app, port=os.getenv("PORT"), host='0.0.0.0', use_reloader=False) # reloader may glitch out mqtt connections?