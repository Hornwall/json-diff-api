import os
from flask import Flask
from flask.ext.cors import CORS
from controllers.index_controller import index_blueprint
from models.repository import Repository
import config

app = Flask(__name__)
CORS(app)
app.debug = True
app.config.from_object(config.Config)
app.register_blueprint(index_blueprint)

if __name__ == "__main__":
    if not os.path.exists(app.config.get("REPOS_DIR_PATH")):
        print("Could not find repos directory, creating it now...")
        os.makedirs(app.config.get("REPOS_DIR_PATH"))
    app.run(host="0.0.0.0")

