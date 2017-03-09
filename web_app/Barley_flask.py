from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
import os
import cPickle as pickle
import requests


# ===== initialize flask app ====
app = Flask(__name__)


# ===== page routing blocks =====
@app.route('/', methods = ['GET','POST'])
def home_page():
    return render_template('index.html')

@app.route('/capstone', methods=['GET'])
def capstone():
    return render_template('capstone.html')

@app.route('/resume', methods=['GET'])
def resume():
    return redirect('http://resumup.com/25278679/online_resume/')

@app.route('/github', methods=['GET'])
def github():
    return redirect('https://github.com/wadere/Barley_Brain')

@app.route('/linkedin', methods=['GET'])
def linkedin():
    return redirect('https://www.linkedin.com/in/wadere/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)