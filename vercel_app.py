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
    # Mock data for Vercel deployment
    mock_notebooks = [
        {
            'id': 1,
            'title': 'CBDC Market Analysis 2024',
            'description': 'Comprehensive analysis of Central Bank Digital Currency adoption trends',
            'author': {'username': 'Analyst1'},
            'created_at': '2024-01-15',
            'views': 1250,
            'likes': 89
        },
        {
            'id': 2,
            'title': 'Stablecoin Performance Metrics',
            'description': 'Real-time analysis of major stablecoin performance and market dynamics',
            'author': {'username': 'CryptoResearcher'},
            'created_at': '2024-01-14',
            'views': 890,
            'likes': 67
        },
        {
            'id': 3,
            'title': 'Regulatory Impact on CBDC Development',
            'description': 'Analysis of global regulatory frameworks and their impact on CBDC projects',
            'author': {'username': 'PolicyAnalyst'},
            'created_at': '2024-01-13',
            'views': 756,
            'likes': 45
        }
    ]
    return render_template('index.html', notebooks=mock_notebooks)

@app.route('/dashboard')
def dashboard():
    # Mock dashboard data
    mock_notebooks = [
        {
            'id': 1,
            'title': 'My CBDC Analysis',
            'description': 'Personal research on CBDC implementation',
            'created_at': '2024-01-15',
            'views': 1250,
            'likes': 89
        }
    ]
    return render_template('dashboard.html', notebooks=mock_notebooks)

@app.route('/upload')
def upload_notebook():
    return render_template('upload.html')

@app.route('/search')
def search_notebooks():
    return render_template('search.html', notebooks=[])

@app.route('/notebook/<int:notebook_id>')
def view_notebook(notebook_id):
    # Mock notebook data
    mock_notebook = {
        'id': notebook_id,
        'title': f'CBDC Analysis Notebook {notebook_id}',
        'description': 'Sample notebook for demonstration purposes',
        'filename': f'notebook_{notebook_id}.ipynb',
        'created_at': '2024-01-15',
        'views': 1250,
        'likes': 89
    }
    
    # Mock notebook content
    mock_content = {
        'cells': [
            {
                'cell_type': 'markdown',
                'source': '# CBDC Market Analysis\n\nThis is a sample notebook for demonstration purposes on Vercel.'
            },
            {
                'cell_type': 'code',
                'source': 'import pandas as pd\nimport matplotlib.pyplot as plt\n\n# Sample data analysis\nprint("CBDC Analysis Complete")',
                'outputs': [
                    {
                        'output_type': 'stream',
                        'name': 'stdout',
                        'text': 'CBDC Analysis Complete'
                    }
                ]
            }
        ]
    }
    
    return render_template('view_notebook.html', notebook=mock_notebook, content=mock_content)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'CBDC/Stablecoin Analysis Dashboard is running on Vercel!'})

if __name__ == '__main__':
    app.run(debug=True)
