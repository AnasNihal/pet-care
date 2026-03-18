from flask import Blueprint, render_template
from app.models import Pet

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get 3 featured available pets
    featured_pets = Pet.query.filter_by(status='available').limit(3).all()
    return render_template('index.html', featured_pets=featured_pets)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')
