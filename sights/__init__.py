from flask import Blueprint

sights = Blueprint('sights', __name__, template_folder='templates/sights', 
                    static_folder='static', static_url_path = "/sights/static",)

# Import views after creating the blueprint to avoid circular imports
from . import views
from . import routes
