from flask import Flask, render_template, request
from api.complexity import get_complexity_analysis

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run()