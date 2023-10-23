from flask import *
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

# Import the blueprint
from general import general 
from sights import sights 
from cart import booking, thankyou 
from auth import auth_obj

# app = Flask(__name__)
app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/static",
)

# Register the blueprint
app.register_blueprint(general) # blueprint registration
app.register_blueprint(sights) # blueprint registration
app.register_blueprint(booking) # blueprint registration
app.register_blueprint(thankyou)
app.register_blueprint(auth_obj)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key = os.getenv('app_secret_key')

# Pages
# @general.route("/")
# def index():
# 	return render_template("index.html")

# @app.route("/attraction/<id>")
# def attraction(id):
# 	return render_template("attraction.html")

# @app.route("/booking")
# def booking():
# 	return render_template("booking.html")

# @app.route("/thankyou")
# def thankyou():
# 	return render_template("thankyou.html")

app.run(host="0.0.0.0", port=3000, debug=True)