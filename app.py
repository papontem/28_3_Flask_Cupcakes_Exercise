"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

# FLASK SETTINGS
app.config["SECRET_KEY"] = "oh-so-secret"
# FLASK-SQLALCHEMY SETTINGS
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# FLASK-DEBUGTOOLBAR SETTINGS
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 

# flask-sqlalchemy init app db
connect_db(app)

