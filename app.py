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

# Part 2: GET and POST
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

## GET /api/cupcakes/<int:cupcake-id>
@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Returns JSON for one cupcake in particular"""

    # Get data about a single cupcake.
    # This should raise a 404 if the cupcake cannot be found.
    cupcake_obj = Cupcake.query.get_or_404(cupcake_id)
    # Serialize the data like: {cupcake: {id, flavor, size, rating, image}}
    cupcake = cupcake_obj.serialize()
    # Respond with JSON by jsonify
    return jsonify(cupcake=cupcake)


## POST /api/cupcakes
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""

    # Create a cupcake with flavor, size, rating and image data from the body of the request.
    new_cupcake = Cupcake( 
        flavor = request.json["flavor"],
        size   = request.json["size"],
        rating = request.json["rating"],
        image  = request.json.get("image")
        )
    

    # add cupcake to db
    db.session.add(new_cupcake)
    db.session.commit()

    # Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


# Part 3: UPDATE(patch) and DELETE
## PATCH /api/cupcakes/<int:cupcake_id>
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def patch_cupcake(cupcake_id):
    """Updates (patch) a particular cupcake and responds w/ JSON of that updated cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # patch the cupcakes data, else use the cupcakes pre set data
    cupcake.flavor = request.json.get( "flavor" , cupcake.flavor )
    cupcake.size   = request.json.get( "size"   , cupcake.size   ) 
    cupcake.rating = request.json.get( "rating" , cupcake.rating )
    cupcake.image  = request.json.get( "image"  , cupcake.image  )
    db.session.commit()
    
    # Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.
    return jsonify(cupcake=cupcake.serialize())


## DELETE /api/cupcakes/<int:cupcake_id>
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a particular cupcake"""
    
    # Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
