import os
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

# Inicializa Flask y SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Variables globales
current_value = 0  # Inicializar en 0
max_progress = 25000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_progress/<int:value>', methods=['GET'])
def update_progress(value):
    global current_value
    current_value = value

    if current_value > max_progress:
        current_value = max_progress
    elif current_value < 0:
        current_value = 0

    percentage = (current_value / max_progress) * 100
    socketio.emit('progress_update', {'percentage': percentage, 'current_value': current_value})

    return {'status': 'success'}

@app.route('/get_current_progress', methods=['GET'])
def get_current_progress():
    """Devuelve el valor actual de la barra de progreso."""
    return jsonify({'current_value': current_value})

if __name__ == '__main__':
    socketio.run(app, debug=True)
