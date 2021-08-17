"""Flask app for Cupcakes"""
from flask import Flask, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hello123'

connect_db(app)


@app.route('/')
def home_rt():
  '''Get home page.'''
  return render_template('home.html')
