from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import nbformat
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notebooks.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    notebooks = db.relationship('Notebook', backref='author', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(500))  # Comma-separated tags
    is_public = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    notebooks = Notebook.query.filter_by(is_public=True).order_by(Notebook.created_at.desc()).limit(12).all()
    return render_template('index.html', notebooks=notebooks)

@app.route('/dashboard')
@login_required
def dashboard():
    user_notebooks = Notebook.query.filter_by(user_id=current_user.id).order_by(Notebook.updated_at.desc()).all()
    return render_template('dashboard.html', notebooks=user_notebooks)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_notebook():
    if request.method == 'POST':
        if 'notebook' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['notebook']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Parse notebook metadata
            try:
                nb = nbformat.read(file_path, as_version=4)
                title = nb.metadata.get('title', filename.replace('.ipynb', ''))
                description = nb.metadata.get('description', '')
            except:
                title = filename.replace('.ipynb', '')
                description = ''
            
            notebook = Notebook(
                title=title,
                description=description,
                filename=filename,
                file_path=file_path,
                tags=request.form.get('tags', ''),
                is_public=request.form.get('is_public') == 'on',
                user_id=current_user.id
            )
            
            db.session.add(notebook)
            db.session.commit()
            
            flash('Notebook uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid file type. Please upload a .ipynb file.', 'error')
    
    return render_template('upload.html')

@app.route('/notebook/<int:notebook_id>')
def view_notebook(notebook_id):
    notebook = Notebook.query.get_or_404(notebook_id)
    
    if not notebook.is_public and (not current_user.is_authenticated or current_user.id != notebook.user_id):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Increment view count
    notebook.views += 1
    db.session.commit()
    
    # Read and parse notebook content
    try:
        nb = nbformat.read(notebook.file_path, as_version=4)
        # Pass the notebook object directly
        notebook_content = nb
    except Exception as e:
        notebook_content = None
        flash(f'Error reading notebook: {str(e)}', 'error')
    
    return render_template('view_notebook.html', notebook=notebook, content=notebook_content)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    tag = request.args.get('tag', '')
    
    if query or tag:
        notebooks = Notebook.query.filter_by(is_public=True)
        
        if query:
            notebooks = notebooks.filter(
                db.or_(
                    Notebook.title.contains(query),
                    Notebook.description.contains(query),
                    Notebook.tags.contains(query)
                )
            )
        
        if tag:
            notebooks = notebooks.filter(Notebook.tags.contains(tag))
        
        notebooks = notebooks.order_by(Notebook.created_at.desc()).all()
    else:
        notebooks = []
    
    return render_template('search.html', notebooks=notebooks, query=query, tag=tag)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/notebooks')
def api_notebooks():
    notebooks = Notebook.query.filter_by(is_public=True).order_by(Notebook.created_at.desc()).limit(20).all()
    return jsonify([{
        'id': nb.id,
        'title': nb.title,
        'description': nb.description,
        'author': nb.author.username,
        'tags': nb.tags.split(',') if nb.tags else [],
        'views': nb.views,
        'likes': nb.likes,
        'created_at': nb.created_at.isoformat()
    } for nb in notebooks])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'ipynb'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")
    app.run(debug=True)
