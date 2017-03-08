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

@app.route('/eda', methods=['GET'])
def eda():
    return render_template('EDA_gov_yields.html')

@app.route('/github', methods=['GET'])
def github():
    return render_template('../static/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)