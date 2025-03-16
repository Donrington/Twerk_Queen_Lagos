from main import app
from flask_socketio import SocketIO

if __name__ == '__main__':
    # Run the app
    socketio = SocketIO(app)
    socketio.run(app, debug=True, port=2025, use_reloader=True)