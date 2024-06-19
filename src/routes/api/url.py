from flask import Blueprint, jsonify, request
from db.main import Database

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
    try:

        is_url = db.url_exists("id", url_id)

        if is_url:
            url = db.get_url(url_id)
            return jsonify(url), 200
        else:
            message_error = {"message": "This URL doesnt exists"}
            return jsonify(message_error), 400

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400


@url_blueprint.route("/url/", methods=["POST"])
def create_url():
    try:

        original_url = request.json["original_url"]

        is_url = db.url_exists("original_url", original_url)

        if is_url:
            message_error = {"message": "This URL exists"}
            return jsonify(message_error), 400
        else:
            new_url = db.create_url(original_url)
            return jsonify(new_url), 201

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400


@url_blueprint.route("/url/<int:url_id>", methods=["DELETE"])
def delete_url(url_id):
    try:

        is_url = db.url_exists("id", url_id)

        if is_url:
            db.delete_url(url_id)
            return jsonify({"message": "Url deleted"}), 200
        else:
            message_error = {"message": "This URL doesnt exists"}
            return jsonify(message_error), 400

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400
