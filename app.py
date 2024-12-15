import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "oden-restaurant-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///oden.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Import models after db initialization
from models import MenuItem, NewsPost, ContactMessage

@app.route('/')
def home():
    featured_items = MenuItem.query.filter_by(featured=True).limit(4).all()
    latest_news = NewsPost.query.order_by(NewsPost.date.desc()).limit(3).all()
    return render_template('home.html', featured_items=featured_items, latest_news=latest_news)

@app.route('/menu')
def menu():
    oden_items = MenuItem.query.filter_by(category='oden').all()
    drinks = MenuItem.query.filter_by(category='drinks').all()
    sides = MenuItem.query.filter_by(category='sides').all()
    return render_template('menu.html', oden_items=oden_items, drinks=drinks, sides=sides)

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/news')
def news():
    posts = NewsPost.query.order_by(NewsPost.date.desc()).all()
    return render_template('news.html', posts=posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            contact_msg = ContactMessage(
                name=name,
                email=email,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('contact.html')

with app.app_context():
    db.create_all()
