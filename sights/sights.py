from . import my_blueprint

@my_blueprint.route('/')
def index():
    return "Hello from my blueprint!"
