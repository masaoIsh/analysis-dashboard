#!/usr/bin/env python3
"""
Initialize the database for the Notebook Dashboard
"""

from app import app, db

with app.app_context():
    print("🗄️  Creating database tables...")
    db.create_all()
    print("✅ Database initialized successfully!")
    print("📁 Database file: notebooks.db")
    print("🚀 You can now run: python run.py")
