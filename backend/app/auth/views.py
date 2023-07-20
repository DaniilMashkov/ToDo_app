from datetime import datetime, timezone, timedelta
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity, set_access_cookies, current_user, unset_jwt_cookies, get_current_user, verify_jwt_in_request
from app.auth import auth
from app.auth.models import User
from app.auth.validators import invalid_form


@auth.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

@auth.route("/verifytoken", methods=["GET"])
@jwt_required(optional=True)
def protected():
    response = jsonify({"msg": "login successful"})
    return response

@auth.route('/login', methods=["POST"])
def login():
    username = request.get_json().get('username')
    user = User.query.filter_by(username=username).one_or_none()

    if invalid := invalid_form(user, request.get_json()):
        response = jsonify({"msg": invalid})
        response.status_code = 400
        return response

    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity=username)

    set_access_cookies(response, access_token)
    return jsonify(token=access_token)

@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
