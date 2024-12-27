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

logger.info(f"Initializing database connection...")

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
        # Test database connection first
        try:
            db.session.execute(text('SELECT 1'))
            logger.info("Database connection test successful")
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            raise

        # Begin a transaction for table creation
        db.session.begin()
        try:
            logger.info("Creating database tables...")
            db.create_all()
            db.session.commit()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {str(e)}")
            db.session.rollback()
            raise

        # Check if tables are empty before adding sample data
        if not MenuItem.query.first() and not NewsPost.query.first() and not Review.query.first():
            logger.info("Tables are empty, adding sample data...")
            try:
                # Sample reviews
                reviews = [
                    Review(
                        author="Nak",
                        content="店主は、塩対応ですが、おでんは美味しいです。ポテトはマックより美味しいです。",
                        image_path="images/reviews/nak.jpg",
                        date=datetime.utcnow()
                    ),
                    Review(
                        author="May",
                        content="店主と仲良くなると出汁もらえます。",
                        image_path="images/reviews/may.jpg",
                        date=datetime.utcnow()
                    ),
                    Review(
                        author="Kom",
                        content="お酒もちゃんと美味しいです。お客さんに合わせた濃淡も考えてくれる店主なのでついついおかわりしてしまいます。",
                        image_path="images/reviews/kom.jpg",
                        date=datetime.utcnow()
                    ),
                    Review(
                        author="Kao",
                        content="マスターも常連さんもみんないい人です。おでんが食べたいなら早めに。",
                        image_path="images/スクリーンショット 2024-12-18 16.05.07.png",
                        date=datetime.utcnow()
                    ),
                    Review(
                        author="Ik",
                        content="アットホームな会社です。",
                        image_path="images/reviews/ik.jpg",
                        date=datetime.utcnow()
                    )
                ]

                # Begin a new transaction for sample data
                db.session.begin()

                try:
                    # Add all sample data
                    for review in reviews:
                        db.session.add(review)
                    logger.info("Added review data")

                    # Sample menu items - Oden
                    oden_items = [
                        MenuItem(name='大根', name_jp='だいこん', description='じっくり煮込んだ大根です', price=200, category='oden', featured=True),
                        MenuItem(name='玉子', name_jp='たまご', description='トロトロの半熟玉子', price=180, category='oden', featured=True),
                        MenuItem(name='こんにゃく', name_jp='こんにゃく', description='歯ごたえのある手作りこんにゃく', price=150, category='oden'),
                        MenuItem(name='牛すじ', name_jp='ぎゅうすじ', description='柔らかく煮込んだ牛すじ', price=300, category='oden', featured=True)
                    ]

                    # Sample menu items - Drinks
                    drinks = [
                        MenuItem(name='生ビール', description='冷えた生ビール', price=500, category='drinks'),
                        MenuItem(name='日本酒', description='地元の銘酒', price=600, category='drinks'),
                        MenuItem(name='焼酎', description='芋焼酎・麦焼酎', price=500, category='drinks')
                    ]

                    # Sample menu items - Sides
                    sides = [
                        MenuItem(name='枝豆', description='塩茹でした枝豆', price=300, category='sides'),
                        MenuItem(name='冷奴', description='冷やっこ', price=250, category='sides'),
                        MenuItem(name='たこわさ', description='新鮮なたこわさび', price=400, category='sides')
                    ]

                    # Add menu items
                    for items in [oden_items, drinks, sides]:
                        for item in items:
                            db.session.add(item)
                    logger.info("Added menu items")

                    # Sample news posts
                    news_posts = [
                        NewsPost(
                            title='年末年始の営業について', 
                            content='12月30日から1月3日まで休業とさせていただきます。',
                            date=datetime.utcnow()
                        ),
                        NewsPost(
                            title='新メニュー追加のお知らせ', 
                            content='季節限定の牛すじおでんが新登場！トロトロに煮込んだ牛すじをぜひご賞味ください。',
                            date=datetime.utcnow()
                        ),
                        NewsPost(
                            title='営業時間変更のお知らせ', 
                            content='12月1日より、営業時間を17時から23時に変更いたしました。',
                            date=datetime.utcnow()
                        )
                    ]

                    # Add news posts
                    for post in news_posts:
                        db.session.add(post)
                    logger.info("Added news posts")

                    # Commit the transaction
                    db.session.commit()
                    logger.info("Successfully committed all sample data")

                except Exception as e:
                    logger.error(f"Error adding sample data: {str(e)}", exc_info=True)
                    db.session.rollback()
                    raise

            except Exception as e:
                logger.error(f"Error during sample data initialization: {str(e)}", exc_info=True)
                raise

        else:
            logger.info("Tables already contain data, skipping sample data insertion")

    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}", exc_info=True)
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
            flash('エラーが発生しました。', 'danger')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)