from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(data):
    print('Received video frame:', data)  # Debug print
    emit('video_frame', data, broadcast=True)
    print('Broadcasted video frame')  # Debug print

@socketio.on('connect')
def connect():
    print('Client connected')  # Debug print
    emit('response', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
