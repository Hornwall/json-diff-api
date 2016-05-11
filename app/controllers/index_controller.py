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
    steps = request.args.get("steps")
    repository = Repository.find(current_app.config.get("REPOS_DIR_PATH"), repository_name)

    if repository:
        if steps:
            if repository.file_exists_in_commit(file_name, steps):
                file_content = repository.get_file_content_from_commit(file_name, steps)
                return render_file_content(file_content)
        else:
            if repository.file_exists(file_name):
                file_content = repository.get_file_content(file_name)
                return render_file_content(file_content)

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

@index_blueprint.route("/<repository_name>/files/<file_name>/diff")
def view_File(repository_name, file_name):
    repository = Repository.find(current_app.config.get("REPOS_DIR_PATH"), repository_name)
    steps = request.args.get("steps")

    if repository:
        if repository.file_exists(file_name):
            if steps:
                return Response(repository.get_file_diff(file_name, steps), mimetype="text/plain")
            else:
                return Response(repository.get_file_diff(file_name, 1), mimetype="text/plain")

    error = { "error": "Not found!" }
    return Response(json.dumps(error, sort_keys=True), mimetype="application/json"), 404

@index_blueprint.route("/<repository_name>/commits")
def list_commits(repository_name):
    amount = request.args.get("amount") or 10
    repository = Repository.find(current_app.config.get("REPOS_DIR_PATH"), repository_name)

    formatted_commits = []

    for index, commit in enumerate(repository.get_commits(amount)):
        commit_object = {}
        commit_object["time"] = datetime.fromtimestamp(commit.committed_date).isoformat()
        commit_object["step"] = index
        formatted_commits.append(commit_object)

    return Response(json.dumps(formatted_commits, sort_keys=True), mimetype="application/json")

def render_file_content(content):
    if isinstance(content, str):
        return Response("{}", mimetype="application/json")
    else:
        return Response(content.decode("utf-8"), mimetype="application/json")

