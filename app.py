import os
import logging
from flask import Flask, render_template
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "a secret key")

# メニューデータ
oden_items = [
    {
        'name': '玉子', 'name_jp': '玉子',
        'description': '出汁がしみ込んだ定番の味',
        'price': 200,
        'image': 'S__135045168_0.jpg'
    },
    {
        'name': '大根', 'name_jp': '大根',
        'description': 'じっくり煮込んだトロトロ大根',
        'price': 200,
        'image': 'S__135045165_0.jpg'
    },
    {
        'name': 'はんぺん', 'name_jp': 'はんぺん',
        'description': 'ふわふわ食感のはんぺん',
        'price': 200,
        'image': 'S__135045163_0.jpg'
    },
    {
        'name': 'こんにゃく', 'name_jp': 'こんにゃく',
        'description': '出汁の旨味が染み込んだこんにゃく',
        'price': 150,
        'image': 'S__135045162_0.jpg'
    },
    {
        'name': 'がんもどき', 'name_jp': 'がんもどき',
        'description': '野菜の旨味が詰まったがんもどき',
        'price': 200,
        'image': 'S__135045160_0.jpg'
    },
    {
        'name': 'キャベツ巻き', 'name_jp': 'キャベツ巻き',
        'description': '新鮮なキャベツで包んだ具材',
        'price': 250,
        'image': 'S__135045159_0.jpg'
    }
]

# Route handlers
@app.route('/')
def home():
    return render_template('home.html', featured_items=[], latest_news=[])

@app.route('/menu')
def menu():
    return render_template('menu.html', oden_items=oden_items, drinks=[], sides=[])

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/news')
def news():
    return render_template('news.html', posts=[])

@app.route('/reviews')
def reviews():
    # Create sample reviews
    sample_reviews = [
        {'author': 'Nak', 'content': '店主は、塩対応ですが、おでんは美味しいです。\nポテトはマックより美味しいです。', 'date': datetime.now()},
        {'author': 'May', 'content': '店主と仲良くなると出汁もらえます。', 'date': datetime.now()},
        {'author': 'Kom', 'content': 'お酒もちゃんと美味しいです。\nお客さんに合わせた濃淡も考えてくれる店主なのでついついおかわりしてしまいます。', 'date': datetime.now()},
        {'author': 'Kao', 'content': 'マスターも常連さんもみんないい人です。\nおでんが食べたいなら早めに。', 'date': datetime.now()},
        {'author': 'Ik', 'content': 'アットホームな会社です。', 'date': datetime.now()},
        {'author': 'MONARIHA', 'content': '店主の魅力にやられてます。', 'date': datetime.now()},
        {'author': 'MOMO', 'content': '美味しいおでんが食べれて、人生のアドバイスもくれます。', 'date': datetime.now()}
    ]
    return render_template('reviews.html', reviews=sample_reviews)

@app.route('/social')
def social():
    return render_template('social.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)