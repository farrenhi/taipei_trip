# # Define routes and views for this blueprint
from flask import *
from . import booking, thankyou

@booking.route("/booking")
def booking():
	return render_template("booking.html")

@thankyou.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")