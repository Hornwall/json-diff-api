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
    if repository:
        changes = {}
        changes["added_documents"] = [change.a_path for change in repository.added_files()]
        changes["deleted_documents"] = [change.a_path for change in repository.deleted_files()]
        changes["modified_documents"] = [change.a_path for change in repository.modified_files()]
        return Response(json.dumps(changes, sort_keys=True), mimetype="application/json")
    else:
        error = { "error": "Not found!" }
        return Response(json.dumps(error, sort_keys=True), mimetype="application/json"), 404

@index_blueprint.route("/<repository_name>/files")
def view_files(repository_name):
    repository = Repository.find(current_app.config.get("REPOS_DIR_PATH"), repository_name)

    if repository:
        return Response(json.dumps(repository.list_files(), sort_keys=True), mimetype="application/json")
    else:
        error = { "error": "Not found!" }
        return Response(json.dumps(error, sort_keys=True), mimetype="application/json"), 404

@index_blueprint.route("/<repository_name>/files/<file_name>")
def view_file(repository_name, file_name):
    repository = Repository.find(current_app.config.get("REPOS_DIR_PATH"), repository_name)

    if repository:
        if repository.file_exists(file_name):
            file_content = repository.get_file_content(file_name)
            if isinstance(file_content, str):
                return Response("{}", mimetype="application/json")
            else:
                return Response(file_content.decode("utf-8"), mimetype="application/json")

    error = { "error": "Not found!" }
    return Response(json.dumps(error, sort_keys=True), mimetype="application/json"), 404

