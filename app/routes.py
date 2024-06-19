from flask import render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.complexity import get_complexity_analysis
from app import app

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per day"]  # Default limit: 10 requests per day per IP
)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per day")
def index():
    complexity = None

    if request.method == 'POST':
        code = request.form['code']
        complexity = get_complexity_analysis(code)
    
    print(complexity)

    return render_template('index.html', complexity=complexity)

@app.route('/stars')
def hall_of_fame():
    return render_template('stars.html')