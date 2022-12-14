import os
from urllib import response
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES

@app.route("/drinks", methods=["GET"])
def drink_list():
    # Get all the drinks from db
    drinks = Drink.query.all()
    return jsonify({"success": True, "drinks": [d.short() for d in drinks]}), 200


@app.route('/drinks')
@requires_auth('get:drinks')
def get_short_drinks(payload):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    })

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_detailed_drinks(payload):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    body = request.get_json()
    try:
        # Prepare Drink for DB
        drink = Drink(title=body.get("title"), recipe=json.dumps(body.get("recipe")))
        # Commit to DB
        drink.insert()

    except Exception:
        abort(400)

    return jsonify({"success": True, "drinks": [drink.long()]})

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_existing_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        body = request.get_json()
        title = body.get('title', None)
        recipe = json.dumps(body.get('recipe', None))
        if title:
            drink.title = title
        if recipe:
            drink.recipe = recipe
        drink.update()
    except:
        abort(500)
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_existing_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        drink.delete()
    except:
        abort(500)
    return jsonify({
        'success': True,
        'delete': id
    })
# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found",
            }
        ),
        404,
    )

@app.errorhandler(403)
def forbidden(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 403,
                "message": "action not allowed",
            }
        ),
        403,
    )

@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request",
            }
        ),
        400,
    )

@app.errorhandler(401)
def unauthorized(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 401,
                "message": "unauthorized",
            }
        ),
        401,
    )
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Receive the raised authorixation error and propagates as response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@app.errorhandler(500)
def server_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error",
            }
        ),
        500,
    )