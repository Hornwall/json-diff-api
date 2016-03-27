from flask import Blueprint, Response, current_app
from models.repository import Repository
from formatters.repository_formatter import RepositoryFormatter
import simplejson as json

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route("/")
def index():
    output = []
    for repository in Repository.all(current_app.config.get("REPOS_DIR_PATH")):
        output.append(RepositoryFormatter.json_format(repository))
    return Response(json.dumps(output, sort_keys=True), mimetype="application/json")

@index_blueprint.route("/<repository_name>")
def view(repository_name):
    repository = Repository.find(current_app.config.get("REPOS_DIR_PATH"), repository_name)
    for change in repository.added_files():
        print(change)

    changes = {}
    changes["added_documents"] = [change.a_path for change in repository.added_files()]
    changes["deleted_documents"] = [change.a_path for change in repository.deleted_files()]
    changes["modified_documents"] = [change.a_path for change in repository.modified_files()]
    return Response(json.dumps(changes, sort_keys=True), mimetype="application/json")

