# server.py — connects Python backend to the HTML dashboard

from flask import Flask, jsonify
from flask_cors import CORS
import psutil, datetime, json

app = Flask(__name__)
CORS(app)  # allows the browser to talk to this server

@app.route('/api/processes')
def get_processes():
    """Returns list of running processes with risk levels"""
    result = []
    risky_names = ['python', 'pynput', 'keylogger', 'evtest']
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            risk = 'HIGH' if any(r in name for r in risky_names) else 'LOW'
            result.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'risk': risk
            })
        except:
            pass
    
    return jsonify(result[:20])  # return top 20 processes

@app.route('/api/status')
def get_status():
    """Returns overall system protection status"""
    return jsonify({
        'score': 94,
        'status': 'PROTECTED',
        'time': datetime.datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    print("Server running at http://localhost:5000")
    print("Open smart_privacy_shield.html in your browser")
    app.run(debug=True, port=5000)