# # Define routes and views for this blueprint
from flask import *
# from flask import Blueprint

# # Create a Blueprint instance
# general = Blueprint('general', __name__)


from . import sights

@sights.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")