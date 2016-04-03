import os
import zipfile
import simplejson as json

from flask import Blueprint, Response, current_app, request
from models.repository import Repository
from formatters.repository_formatter import RepositoryFormatter
from datetime import datetime

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

@index_blueprint.route("/<repository_name>/update", methods=["post"])
def updated_repository(repository_name):
    repository_path = os.path.join(current_app.config.get("REPOS_DIR_PATH"), repository_name)

    repository = Repository.find_or_create(current_app.config.get("REPOS_DIR_PATH"), repository_name)
    zip_file = zipfile.ZipFile(request.files["file"])

    for name in [name for name in os.listdir(repository_path) if name != ".git"]:
            os.remove(os.path.join(repository_path, name))

    zip_file.extractall(repository_path)

    repository.repo.git.add(A=True)
    try:
        repository.repo.git.commit(m=datetime.today().strftime("%s"))
    except:
        return "No changes where made"

    return "updated"
