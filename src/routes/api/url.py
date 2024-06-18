from flask import Blueprint, jsonify, request
from db.pgsql import Database

url_blueprint = Blueprint(
    "url",
    __name__,
)

db = Database()
db.start()


@url_blueprint.route("/url/", methods=["GET"])
def get_urls():
    urls = db.get_urls()
    return jsonify(urls)


@url_blueprint.route("/url/<int:url_id>", methods=["GET"])
def get_url(url_id):
    url = db.get_url(url_id)
    return jsonify(url)


@url_blueprint.route("/url/", methods=["POST"])
def create_url():
    try:
        original_url = request.json["original_url"]

        new_url = db.create_url(original_url)
        return jsonify(new_url), 201
    except:
        message_error = {"message": "Error"}
        return jsonify(message_error), 400


@url_blueprint.route("/url/<int:id>", methods=["DELETE"])
def delete_url(id):
    try:
        db.delete_url(id)
        return jsonify({"message": "Url deleted"}), 200
    except:
        message_error = {"message": "Error"}
        return jsonify(message_error), 400
