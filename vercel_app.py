#!/usr/bin/env python3
"""
Vercel-compatible Flask application for CBDC/Stablecoin Analysis Dashboard
This is a simplified version that works on Vercel's serverless environment
"""

from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Routes
@app.route('/')
def index():
    return jsonify({
        'message': 'CBDC/Stablecoin Analysis Dashboard',
        'status': 'running',
        'deployment': 'vercel'
    })

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'CBDC/Stablecoin Analysis Dashboard is running on Vercel!'})

@app.route('/test')
def test():
    return jsonify({'test': 'success', 'platform': 'vercel'})

if __name__ == '__main__':
    app.run(debug=True)
