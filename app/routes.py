from flask import render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from app.complexity import get_complexity_analysis
from app.utils.leetcode import get_leetcode_user_stats
from app import app
import json

config = {
    'DEBUG': True,
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
}

cache = Cache(config=config)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per day"]  # Default limit: 10 requests per day per IP
)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per day")
def index():
    complexity = None

    if request.method == 'POST':
        code = request.form['code']
        complexity = get_complexity_analysis(code)

    return render_template('index.html', complexity = complexity)

@app.route('/stars', methods=['GET'])
def hall_of_fame():
    with open('stars.json', 'r') as f:
        stars = json.load(f)
    return render_template('stars.html', stars = stars)
 
@cache.cached(timeout=300)
@app.route('/profile/<username>', methods=['GET'])
def leetcode_profile(username):
    profile_data = get_leetcode_user_stats(username)
    return render_template('profile.html', profile_data = profile_data)