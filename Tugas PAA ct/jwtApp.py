from flask import Flask, make_response #import library
from flask import jsonify #import library
from flask import request #import library

from flask_jwt_extended import create_access_token #import library
from flask_jwt_extended import get_jwt_identity #import library
from flask_jwt_extended import jwt_required #import library
from flask_jwt_extended import JWTManager #import library

app = Flask(__name__, static_url_path='/static') #menuju url static

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "myjwtsecretkey"  # Mengatur secret key
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"] # Tempat program akan mengakses jwt
jwt = JWTManager(app)
account = { #membuat account
    "username": "test",
    "password": "test",
}



# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"]) #bikin route menuju login dgn method post
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != account["username"] or password != account["password"]:
        return jsonify({"message": "Bad username or password"}), 401

    access_token = create_access_token(identity=account) # Men-generate access token
    response = make_response(jsonify(access_token=access_token), 200) #Membuat response dengan isi tokennya
    response.set_cookie('access_token_cookie', access_token) # Mengirimkan cookie ke client dengan isi token yg sudah dibuat
    return response



# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/",methods=["GET"])
def mainPage():
    return 200


if __name__ == "__main__":
    app.run(port=5000)


