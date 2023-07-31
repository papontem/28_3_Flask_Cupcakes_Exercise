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


# ************************************************************
#         VVV RESTFUL CUPCAKE JSON API ROUTES VVV
#   Make sure flask is running before using the api routes
# ************************************************************
## GET /api/cupcakes
@app.route("/api/cupcakes")
def get_all_cupcakes_list():
    """Returns JSON w/ all cupcakes"""

    # Get data about all cupcakes.
    # The values should come from each cupcake instance.
    # Serialize the data like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    # Respond with JSON by jsonify
    return jsonify(cupcakes=all_cupcakes)

