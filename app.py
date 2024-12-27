import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Create the Flask app first
app = Flask(__name__)

# Secret key configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "a secret key")

# Database configuration
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    logger.error("DATABASE_URL environment variable is not set")
    raise ValueError("DATABASE_URL environment variable is required")

# Fix potential incompatibility with some database URLs
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

logger.info(f"Configuring database connection...")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Initialize the app with the extension
try:
    db.init_app(app)
    logger.info("Successfully initialized database with Flask app")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
    raise

# Import models after db initialization
from models import MenuItem, NewsPost, ContactMessage, Review

# Create database tables
with app.app_context():
    try:
        # Test database connection
        logger.info("Testing database connection...")
        result = db.session.execute(text('SELECT 1'))
        result.scalar()
        logger.info("Database connection test successful")

        # Create tables
        db.create_all()
        logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}", exc_info=True)
        raise

# Route handlers
@app.route('/')
def home():
    try:
        featured_items = MenuItem.query.filter_by(featured=True).all()
        latest_news = NewsPost.query.order_by(NewsPost.date.desc()).limit(3).all()
        return render_template('home.html', featured_items=featured_items, latest_news=latest_news)
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}", exc_info=True)
        return "An error occurred", 500

@app.route('/menu')
def menu():
    try:
        oden_items = MenuItem.query.filter_by(category='oden').all()
        drinks = MenuItem.query.filter_by(category='drinks').all()
        sides = MenuItem.query.filter_by(category='sides').all()
        return render_template('menu.html', oden_items=oden_items, drinks=drinks, sides=sides)
    except Exception as e:
        logger.error(f"Error in menu route: {str(e)}", exc_info=True)
        return "An error occurred", 500

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/news')
def news():
    try:
        posts = NewsPost.query.order_by(NewsPost.date.desc()).all()
        return render_template('news.html', posts=posts)
    except Exception as e:
        logger.error(f"Error in news route: {str(e)}", exc_info=True)
        return "An error occurred", 500

@app.route('/reviews')
def reviews():
    try:
        reviews = Review.query.order_by(Review.date.desc()).all()
        return render_template('reviews.html', reviews=reviews)
    except Exception as e:
        logger.error(f"Error in reviews route: {str(e)}", exc_info=True)
        return "An error occurred", 500

@app.route('/social')
def social():
    return render_template('social.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            if not all([name, email, message]):
                flash('全ての項目を入力してください。', 'danger')
            else:
                contact_message = ContactMessage(
                    name=name,
                    email=email,
                    message=message
                )
                db.session.add(contact_message)
                db.session.commit()
                flash('お問い合わせありがとうございます。', 'success')
                return redirect(url_for('contact'))
        except Exception as e:
            logger.error(f"Error in contact form submission: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('エラーが発生しました。', 'danger')
        finally:
            db.session.close()

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)