# CBDC/Stablecoin Analysis Dashboard

A modern web application for sharing and analyzing Jupyter notebooks focused on Central Bank Digital Currencies (CBDCs) and Stablecoin research.

## 🚀 Features

- **Interactive Dashboard**: Real-time charts and metrics for CBDC/Stablecoin markets
- **Notebook Sharing**: Upload and share Jupyter notebooks, Google Colab files, and Python scripts
- **User Authentication**: Secure user registration and login system
- **Search & Discovery**: Find analysis notebooks by tags and content
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Charts**: Interactive visualizations using Chart.js

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js for data visualization
- **Authentication**: Flask-Login
- **Styling**: Custom CSS with responsive design

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/masaoIsh/analysis-dashboard.git
cd analysis-dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Run the Application
```bash
python run.py
```

### 5. Open Your Browser
Navigate to `http://localhost:5001`

## 📁 Project Structure

```
analysis-dashboard/
├── app.py                 # Main Flask application
├── run.py                 # Application entry point
├── init_db.py            # Database initialization script
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with sidebar
│   ├── index.html        # Dashboard homepage
│   ├── login.html        # User login page
│   ├── register.html     # User registration page
│   ├── dashboard.html    # User dashboard
│   ├── upload.html       # Notebook upload page
│   ├── search.html       # Search results page
│   └── view_notebook.html # Notebook viewer
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # Client-side JavaScript
└── README.md             # This file
```

## 🔧 Configuration

The application uses the following default settings:
- **Port**: 5001 (configurable in `run.py`)
- **Database**: SQLite (`notebooks.db`)
- **Debug Mode**: Enabled for development

## 📊 Dashboard Features

### Key Metrics
- Total Market Cap
- CBDC Projects Count
- Stablecoin Volume
- Active Users

### Interactive Charts
- Market Cap Distribution (Doughnut Chart)
- CBDC Adoption Timeline (Line Chart)
- Top Stablecoins Performance (Bar Chart)

### Analysis Notebooks
- Browse latest research and analysis
- Search by tags and content
- View notebook outputs and visualizations

## 👥 User Features

### Authentication
- User registration and login
- Secure password hashing
- Session management

### Notebook Management
- Upload Jupyter notebooks (.ipynb)
- Support for Google Colab files
- Python script uploads (.py)
- Tag-based organization
- Public/private visibility settings

### Dashboard
- Personal notebook collection
- Upload history
- Usage statistics

## 🎨 Design Features

- **Modern UI**: Clean, minimalist design
- **Responsive Layout**: Works on all device sizes
- **Left Sidebar Navigation**: Easy access to all features
- **Interactive Elements**: Hover effects and smooth transitions
- **Professional Look**: Suitable for financial analysis

## 🔒 Security Features

- Secure file uploads with filename sanitization
- User authentication and session management
- Input validation and sanitization
- SQL injection protection via SQLAlchemy

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include your environment details and error messages

## 🔮 Future Enhancements

- Real-time data feeds for CBDC/Stablecoin metrics
- Advanced charting and analytics tools
- Collaborative editing features
- API endpoints for external integrations
- Mobile app development
- Advanced search and filtering
- Export functionality for analysis reports

---

**Built with ❤️ for the CBDC and Stablecoin research community**
