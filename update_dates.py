#!/usr/bin/env python3
"""
Update all notebook dates to 2025-09-20
"""

from app import app, db, Notebook
from datetime import datetime

def update_dates():
    with app.app_context():
        # Update all notebooks to have the same date
        new_date = datetime(2025, 9, 20)
        
        notebooks = Notebook.query.all()
        for notebook in notebooks:
            notebook.created_at = new_date
            notebook.updated_at = new_date
        
        db.session.commit()
        
        print(f"✅ Updated {len(notebooks)} notebooks to date: 2025-09-20")
        print(f"📊 Total notebooks in database: {Notebook.query.count()}")

if __name__ == '__main__':
    update_dates()
