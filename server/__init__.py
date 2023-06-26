# importing app here because it contains the flask startup pieces necessary for
# "flask --app [app_name] run --host=0.0.0.0" to run properly
from .app import app as flask_app
