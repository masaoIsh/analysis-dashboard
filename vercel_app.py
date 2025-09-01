#!/usr/bin/env python3
"""
Vercel-compatible Flask application for CBDC/Stablecoin Analysis Dashboard
This version serves the full dashboard HTML for Vercel deployment
"""

from flask import Flask, render_template_string, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Mock data for the dashboard
MOCK_NOTEBOOKS = [
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
        'title': 'Stablecoin Regulation Impact',
        'description': 'Analysis of regulatory changes on stablecoin markets and DeFi protocols',
        'author': {'username': 'RegExpert'},
        'created_at': '2024-01-10',
        'views': 890,
        'likes': 67
    },
    {
        'id': 3,
        'title': 'Digital Yuan Implementation',
        'description': 'Technical deep-dive into China\'s CBDC infrastructure and adoption',
        'author': {'username': 'TechAnalyst'},
        'created_at': '2024-01-08',
        'views': 1100,
        'likes': 92
    }
]

# Dashboard HTML template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBDC/Stablecoin Analysis Dashboard</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            line-height: 1.6;
        }
        
        .app-container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 280px;
            background: white;
            border-right: 1px solid #e9ecef;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }
        
        .sidebar-header {
            padding: 24px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: #333;
            font-size: 18px;
            font-weight: 600;
        }
        
        .logo i {
            font-size: 24px;
            color: #007bff;
        }
        
        .sidebar-nav {
            padding: 24px 0;
        }
        
        .nav-item {
            display: block;
            padding: 12px 24px;
            color: #666;
            text-decoration: none;
            transition: all 0.2s ease;
        }
        
        .nav-item:hover {
            background: #f8f9fa;
            color: #007bff;
        }
        
        .nav-item.active {
            background: #e3f2fd;
            color: #007bff;
            border-right: 3px solid #007bff;
        }
        
        .main-content {
            flex: 1;
            margin-left: 280px;
            background-color: white;
            overflow-x: hidden;
            max-width: calc(100vw - 280px);
            box-sizing: border-box;
        }
        
        .content-wrapper {
            padding: 32px;
            max-width: 100%;
            box-sizing: border-box;
            overflow-x: hidden;
        }
        
        .dashboard-header {
            background: white;
            color: #333;
            padding: 40px 32px;
            border-radius: 16px;
            margin-bottom: 32px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            max-width: 100%;
            box-sizing: border-box;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 24px;
        }
        
        .header-info h1 {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header-info p {
            font-size: 16px;
            color: #666;
        }
        
        .time-select {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            color: #333;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
        }
        
        .metrics-dashboard {
            margin-bottom: 32px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 24px;
            max-width: 100%;
            box-sizing: border-box;
        }
        
        .metric-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .metric-card.primary {
            background: #007bff;
            color: white;
        }
        
        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .metric-header h3 {
            font-size: 14px;
            font-weight: 500;
            opacity: 0.8;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .metric-change {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .metric-change.positive {
            color: #28a745;
        }
        
        .metric-change.negative {
            color: #dc3545;
        }
        
        .charts-section {
            margin-bottom: 32px;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
        }
        
        @media (min-width: 1200px) {
            .charts-grid {
                grid-template-columns: 2fr 1fr 1fr;
            }
        }
        
        .chart-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .chart-header h3 {
            font-size: 18px;
            font-weight: 600;
        }
        
        .chart-actions {
            display: flex;
            gap: 8px;
        }
        
        .chart-btn {
            padding: 8px 16px;
            border: 1px solid #dee2e6;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        
        .chart-btn.active {
            background: #007bff;
            color: white;
            border-color: #007bff;
        }
        
        .chart-container {
            height: 300px;
            position: relative;
        }
        
        .analysis-section {
            margin-bottom: 32px;
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        
        .section-header h2 {
            font-size: 24px;
            font-weight: 600;
        }
        
        .upload-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .upload-btn:hover {
            background: #0056b3;
            transform: translateY(-1px);
        }
        
        .notebooks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 24px;
        }
        
        .notebook-card {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 24px;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .notebook-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .notebook-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .notebook-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        
        .notebook-description {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        
        .notebook-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: #999;
        }
        
        .quick-stats {
            margin-top: 32px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        
        .stat-item {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            text-align: center;
        }
        
        .stat-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #333;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                position: relative;
                height: auto;
            }
            
            .main-content {
                margin-left: 0;
                max-width: 100vw;
            }
            
            .app-container {
                flex-direction: column;
            }
            
            .dashboard-header {
                padding: 24px 20px;
                margin: 16px;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
                gap: 16px;
                margin: 0 16px;
            }
            
            .chart-card {
                padding: 20px;
                margin: 0 16px;
            }
            
            .charts-section {
                margin: 0 16px 32px 16px;
            }
            
            .analysis-section {
                margin: 0 16px 32px 16px;
            }
            
            .quick-stats {
                margin: 0 16px;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <a href="/" class="logo">
                    <i class="fas fa-coins"></i>
                    <span>CBDC/Stablecoin Analysis</span>
                </a>
            </div>
            <nav class="sidebar-nav">
                <a href="/" class="nav-item active">
                    <i class="fas fa-chart-line"></i> Dashboard
                </a>
                <a href="/upload" class="nav-item">
                    <i class="fas fa-upload"></i> Share Analysis
                </a>
                <a href="/search" class="nav-item">
                    <i class="fas fa-search"></i> Search
                </a>
                <a href="/dashboard" class="nav-item">
                    <i class="fas fa-user"></i> My Dashboard
                </a>
            </nav>
        </aside>
        
        <!-- Main Content -->
        <main class="main-content">
            <div class="content-wrapper">
                <!-- Dashboard Header -->
                <div class="dashboard-header">
                    <div class="header-content">
                        <div class="header-info">
                            <h1>CBDC/Stablecoin Analysis</h1>
                            <p>Real-time insights into Central Bank Digital Currencies and Stablecoin markets</p>
                        </div>
                        <div class="header-actions">
                            <div class="time-filter">
                                <select id="timeFilter" class="time-select">
                                    <option value="1d">Last 24 Hours</option>
                                    <option value="7d" selected>Last 7 Days</option>
                                    <option value="30d">Last 30 Days</option>
                                    <option value="90d">Last 90 Days</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Key Metrics Dashboard -->
                <div class="metrics-dashboard">
                    <div class="metrics-grid">
                        <div class="metric-card primary">
                            <div class="metric-header">
                                <h3>Total Market Cap</h3>
                                <i class="fas fa-chart-line"></i>
                            </div>
                            <div class="metric-value">$2.4T</div>
                            <div class="metric-change positive">
                                <i class="fas fa-arrow-up"></i>
                                +5.2%
                            </div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-header">
                                <h3>CBDC Projects</h3>
                                <i class="fas fa-building"></i>
                            </div>
                            <div class="metric-value">87</div>
                            <div class="metric-change positive">
                                <i class="fas fa-arrow-up"></i>
                                +3
                            </div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-header">
                                <h3>Stablecoin Volume</h3>
                                <i class="fas fa-exchange-alt"></i>
                            </div>
                            <div class="metric-value">$89.2B</div>
                            <div class="metric-change negative">
                                <i class="fas fa-arrow-down"></i>
                                -2.1%
                            </div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-header">
                                <h3>Active Users</h3>
                                <i class="fas fa-users"></i>
                            </div>
                            <div class="metric-value">12.4M</div>
                            <div class="metric-change positive">
                                <i class="fas fa-arrow-up"></i>
                                +8.7%
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Charts Section -->
                <div class="charts-section">
                    <div class="charts-grid">
                        <!-- Market Cap Distribution Chart -->
                        <div class="chart-card large">
                            <div class="chart-header">
                                <h3>Market Cap Distribution</h3>
                                <div class="chart-actions">
                                    <button class="chart-btn active" data-chart="market-cap">Market Cap</button>
                                    <button class="chart-btn" data-chart="volume">Volume</button>
                                </div>
                            </div>
                            <div class="chart-container">
                                <canvas id="marketCapChart" width="400" height="200"></canvas>
                            </div>
                        </div>
                        
                        <!-- CBDC Adoption Timeline -->
                        <div class="chart-card">
                            <div class="chart-header">
                                <h3>CBDC Adoption Timeline</h3>
                                <i class="fas fa-calendar-alt"></i>
                            </div>
                            <div class="chart-container">
                                <canvas id="adoptionChart" width="300" height="200"></canvas>
                            </div>
                        </div>
                        
                        <!-- Stablecoin Performance -->
                        <div class="chart-card">
                            <div class="chart-header">
                                <h3>Top Stablecoins</h3>
                                <i class="fas fa-coins"></i>
                            </div>
                            <div class="chart-container">
                                <canvas id="stablecoinChart" width="300" height="200"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Analysis Notebooks -->
                <div class="analysis-section">
                    <div class="section-header">
                        <h2>Latest Analysis</h2>
                        <div class="section-actions">
                            <a href="/upload" class="upload-btn">
                                <i class="fas fa-plus"></i>
                                Share Analysis
                            </a>
                        </div>
                    </div>
                    
                    <div class="notebooks-grid">
                        {% for notebook in notebooks %}
                        <div class="notebook-card">
                            <div class="notebook-header">
                                <div>
                                    <h3 class="notebook-title">{{ notebook.title }}</h3>
                                    <p class="notebook-description">{{ notebook.description }}</p>
                                </div>
                            </div>
                            <div class="notebook-meta">
                                <span>By {{ notebook.author.username }}</span>
                                <span>{{ notebook.created_at }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <!-- Quick Stats -->
                <div class="quick-stats">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-label">Total Analysis</div>
                            <div class="stat-value">{{ notebooks|length }}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Contributors</div>
                            <div class="stat-value">{{ notebooks|map(attribute='author.username')|unique|list|length }}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Total Views</div>
                            <div class="stat-value">{{ notebooks|sum(attribute='views') }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script>
        // Initialize Dashboard Charts
        document.addEventListener('DOMContentLoaded', function() {
            createMarketCapChart();
            createAdoptionChart();
            createStablecoinChart();
            initializeChartButtons();
        });
        
        function createMarketCapChart() {
            const ctx = document.getElementById('marketCapChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['USDT', 'USDC', 'BUSD', 'DAI', 'Other'],
                    datasets: [{
                        data: [45, 25, 15, 10, 5],
                        backgroundColor: [
                            '#26A69A',
                            '#2196F3',
                            '#FFC107',
                            '#4CAF50',
                            '#9E9E9E'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true
                            }
                        }
                    }
                }
            });
        }
        
        function createAdoptionChart() {
            const ctx = document.getElementById('adoptionChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['2020', '2021', '2022', '2023', '2024', '2025'],
                    datasets: [{
                        label: 'CBDC Projects',
                        data: [12, 25, 45, 67, 78, 87],
                        borderColor: '#2196F3',
                        backgroundColor: 'rgba(33, 150, 243, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                display: false
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
        
        function createStablecoinChart() {
            const ctx = document.getElementById('stablecoinChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['USDT', 'USDC', 'BUSD', 'DAI'],
                    datasets: [{
                        label: 'Market Cap ($B)',
                        data: [95.2, 52.8, 15.6, 8.4],
                        backgroundColor: [
                            '#26A69A',
                            '#2196F3',
                            '#FFC107',
                            '#4CAF50'
                        ],
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                display: false
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
        
        function initializeChartButtons() {
            const chartBtns = document.querySelectorAll('.chart-btn');
            chartBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    // Remove active class from all buttons
                    chartBtns.forEach(b => b.classList.remove('active'));
                    // Add active class to clicked button
                    this.classList.add('active');
                    
                    // TODO: Implement chart switching logic
                    console.log('Switching to:', this.getAttribute('data-chart'));
                });
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, notebooks=MOCK_NOTEBOOKS)

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'CBDC/Stablecoin Analysis Dashboard is running on Vercel!'})

@app.route('/upload')
def upload():
    return jsonify({'message': 'Upload functionality would be available in the full version'})

@app.route('/search')
def search():
    return jsonify({'message': 'Search functionality would be available in the full version'})

@app.route('/dashboard')
def dashboard():
    return jsonify({'message': 'User dashboard would be available in the full version'})

if __name__ == '__main__':
    app.run()
