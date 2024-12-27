import os
import logging
from flask import Flask, render_template

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "a secret key")

# Route handlers
@app.route('/')
def home():
    return render_template('home.html', featured_items=[], latest_news=[])

@app.route('/menu')
def menu():
    return render_template('menu.html', oden_items=[], drinks=[], sides=[])

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/news')
def news():
    return render_template('news.html', posts=[])

@app.route('/reviews')
def reviews():
    return render_template('reviews.html', reviews=[])

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