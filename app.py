from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/theater')
def theater():
    return render_template('theater.html')

@app.route('/spectacle')
def spectacle():
    return render_template('spectacle.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


if __name__ == '__main__':
    app.run(debug=True)
