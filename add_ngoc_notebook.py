#!/usr/bin/env python3
"""
Add Ngoc-DAI notebook to the database
"""

from app import app, db, Notebook, User

def add_ngoc_notebook():
    with app.app_context():
        # Get admin user
        admin_user = User.query.first()
        if not admin_user:
            print("❌ No admin user found. Please run the app first to create a user.")
            return
        
        # Check if Ngoc-DAI notebook already exists
        existing = Notebook.query.filter_by(title='Ngoc - DAI Analysis').first()
        if existing:
            print("✅ Ngoc-DAI notebook already exists")
            return
        
        # Create new notebook
        notebook = Notebook(
            title='Ngoc - DAI Analysis',
            description='Analysis of DAI stablecoin by Ngoc',
            filename='external_colab.ipynb',
            file_path='',
            external_url='https://colab.research.google.com/drive/1OiGcsfKAqWxppyrtdWjYHRRqa-xYVMfs#scrollTo=ucp0YmYX5LG0',
            author_name='Ngoc',
            tags='stablecoin,dai,ngoc,external',
            is_public=True,
            user_id=admin_user.id
        )
        
        db.session.add(notebook)
        db.session.commit()
        
        print("✅ Successfully added Ngoc-DAI notebook to database")
        print(f"📊 Total notebooks in database: {Notebook.query.count()}")

if __name__ == '__main__':
    add_ngoc_notebook()
