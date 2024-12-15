import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///oden.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

from models import MenuItem, NewsPost, ContactMessage

@app.route('/')
def home():
    featured_items = MenuItem.query.filter_by(featured=True).all()
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
@app.route('/social')
def social():
    return render_template('social.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
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
            
    return render_template('contact.html')

def add_sample_data():
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
    
    # Sample news posts
    news_posts = [
        NewsPost(title='年末年始の営業について', 
                content='12月30日から1月3日まで休業とさせていただきます。'),
        NewsPost(title='新メニュー追加のお知らせ', 
                content='季節限定の牛すじおでんが新登場！トロトロに煮込んだ牛すじをぜひご賞味ください。'),
        NewsPost(title='営業時間変更のお知らせ', 
                content='12月1日より、営業時間を17時から23時に変更いたしました。')
    ]
    
    # Add all items to database
    for items in [oden_items, drinks, sides]:
        for item in items:
            existing = MenuItem.query.filter_by(name=item.name).first()
            if not existing:
                db.session.add(item)
    
    for post in news_posts:
        existing = NewsPost.query.filter_by(title=post.title).first()
        if not existing:
            db.session.add(post)
    
    db.session.commit()

with app.app_context():
    db.create_all()
    add_sample_data()
