from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/')
def hello():
    """Main endpoint that will automatically create traces"""
    return jsonify({
        'message': 'Hello from AWS App Runner!',
        'service': os.environ.get('DD_SERVICE', 'simple-trace-app'),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)