#!/usr/bin/env python3
"""6. Basic Flask app"""
from auth import Auth
from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   redirect)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def helloWorld() -> str:
    """hello world"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """register a user"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    msg = {"email": email, "message": "user created"}
    return jsonify(msg)


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """login in a user"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    sess_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    resp = jsonify(msg)
    resp.set_cookie("session_id", sess_id)
    return resp

@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """logout the user"""
    sess_id = request.cookies.get("session_id", None)
    if sess_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(sess_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')

@app.route('/profile', methods=['GET'])
def profile() -> str:
    """if user exist return 200 http status and json payload"""
    sess_id = request.cookies.get("session_id",None)
    if sess_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(sess_id)
    if user is None:
        abort(403)
    msg = {"email": user.email}
    return jsonify(msg), 200

#     msg = {"email": user.email}

#     return jsonify(msg), 200


# @app.route('/reset_password', methods=['POST'])
# def reset_password() -> str:
#     """If the email is not registered, respond with a 403 status code.
#     Otherwise, generate a token and respond with a
#     200 HTTP status and JSON Payload
#     """
#     try:
#         email = request.form['email']
#     except KeyError:
#         abort(403)

#     try:
#         reset_token = AUTH.get_reset_password_token(email)
#     except ValueError:
#         abort(403)

#     msg = {"email": email, "reset_token": reset_token}

#     return jsonify(msg), 200


# @app.route('/reset_password', methods=['PUT'])
# def update_password() -> str:
#     """ PUT /reset_password
#     Updates password with reset token
#     Return:
#         - 400 if bad request
#         - 403 if not valid reset token
#         - 200 and JSON Payload if valid
#     """
#     try:
#         email = request.form['email']
#         reset_token = request.form['reset_token']
#         new_password = request.form['new_password']
#     except KeyError:
#         abort(400)

#     try:
#         AUTH.update_password(reset_token, new_password)
#     except ValueError:
#         abort(403)

#     msg = {"email": email, "message": "Password updated"}
#     return jsonify(msg), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
