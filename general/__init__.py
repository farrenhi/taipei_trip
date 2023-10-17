from flask import Blueprint

general = Blueprint('general', __name__, template_folder='templates/general', 
                    static_folder='static', static_url_path = "/general/static",)

# Import views after creating the blueprint to avoid circular imports
from . import views
