from flask import Flask, request, jsonify
from flask_cors import CORS
from graph import ResourceAllocationGraph
import logging

app = Flask(__name__)

# Enhanced CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://deadlock-p4ty.onrender.com",
            "http://localhost:5173"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True,
        "max_age": 600
    }
})

@app.after_request
def add_cors_headers(response):
    # Dynamically set allowed origin
    allowed_origins = [
        "https://deadlock-p4ty.onrender.com",
        "http://localhost:5173"
    ]
    origin = request.headers.get('Origin')
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# [Keep all your existing routes unchanged]
