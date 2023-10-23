from flask import Blueprint

booking = Blueprint('booking', __name__, template_folder='templates/cart', 
                    static_folder='static', static_url_path = "/cart/static",)


thankyou = Blueprint('thankyou', __name__, template_folder='templates/cart', 
                    static_folder='static', static_url_path = "/cart/static",)


from . import views

from . import routes