# # Define routes and views for this blueprint
from flask import *
# from flask import Blueprint

# # Create a Blueprint instance
# general = Blueprint('general', __name__)


from . import booking, thankyou


@booking.route("/booking")
def booking():
	return render_template("booking.html")

@thankyou.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")