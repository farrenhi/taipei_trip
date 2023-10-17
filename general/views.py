# # Define routes and views for this blueprint
from flask import *
# from flask import Blueprint

# # Create a Blueprint instance
# general = Blueprint('general', __name__)


from . import general

# Define routes and views for this blueprint
@general.route("/")
def index():
	return render_template("index.html")