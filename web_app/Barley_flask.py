from flask import Flask, render_template, url_for, redirect
import os
import cPickle as pickle
import requests


# ===== initialize flask app ====
app = Flask(__name__)


# ===== page routing blocks =====
@app.route('/', methods = ['GET','POST'])
def home_page():
    return render_template('index.html')

@app.route('/score', methods=['GET,POST'])
def score():
    return '''
    <h2>Barley Brain!</h2>
    <img src='../../images/model_performance_train.jpg>
    '''




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)