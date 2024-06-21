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

        url_exists = db.url_exists("id", url_id)

        if url_exists:
            url = db.get_url("id",url_id)
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

        protocol, https = "https://", original_url[:8]
            
        is_url = True if https == protocol else False     
        
        url_exists = db.url_exists("original_url", original_url)

        if is_url:
            if url_exists:
                url = db.get_url("original_url", original_url)
                message = {"message":"This URL exists" , "data": url}
                return jsonify(message), 200
            else:
                new_url = db.create_url(original_url)
                return jsonify(new_url), 200
        else:
            message_error = {"message": "This not longer an URL"}
            return jsonify(message_error), 400

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400


@url_blueprint.route("/url/<int:url_id>", methods=["DELETE"])
def delete_url(url_id):
    try:

        url_exists = db.url_exists("id", url_id)

        if url_exists:
            db.delete_url(url_id)
            return jsonify({"message": "Url deleted"}), 200
        else:
            message_error = {"message": "This URL doesnt exists"}
            return jsonify(message_error), 400

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400
