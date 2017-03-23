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

@app.route('/template', methods=['GET'])
def template():
    return render_template('template.html')

@app.route('/landsat', methods=['GET'])
def landsat():
    return redirect('https://www.nasa.gov/mission_pages/landsat/overview/index.html')

@app.route('/github', methods=['GET'])
def github():
    return redirect('https://github.com/wadere/BarleyBrain')

@app.route('/github_h', methods=['GET'])
def github_h():
    return redirect('https://github.com/wadere')

@app.route('/linkedin', methods=['GET'])
def linkedin():
    return redirect('https://www.linkedin.com/in/wadere')

@app.route('/NASS', methods=['GET'])
def nass():
    return redirect('https://www.nass.usda.gov')

@app.route('/darksky', methods=['GET'])
def darksky():
    return redirect('https://www.darksky.net')


@app.route('/galvanize', methods=['GET'])
def galvanize():
    return redirect('https://talent.galvanize.com')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)