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
            situation = 'URL_EXISTS'
        else:
            situation = 'URL_NOT_EXISTS'
            
        
        match situation:
            case 'URL_EXISTS':
                url = db.get_url("id",url_id)
                return jsonify(url), 200
            case 'URL_NOT_EXISTS':
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
        
        decent_num_char = len(original_url) < 255
    
        situation = None
        
        if decent_num_char:
            if is_url:
                if url_exists:
                    situation = 'URL_EXISTS'
                else:                    
                    situation = 'URL_NOT_EXISTS'
            else:                
                situation = 'IS_NOT_URL'
        else:
            situation = 'MAX_LENGTH'

        
        match situation:
            case 'URL_EXISTS':
                url = db.get_url("original_url", original_url)
                message = {"message":"This URL exists" , "data": url}
                return jsonify(message), 200
            case 'URL_NOT_EXISTS':
                new_url = db.create_url(original_url)
                return jsonify(new_url), 200
            case 'IS_NOT_URL':
                message_error = {"message": "This not longer an URL"}
                return jsonify(message_error), 400
            case 'MAX_LENGTH':
                message_error = {"message": "Max 255 charapters"}
                return jsonify(message_error), 400
            


    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400


@url_blueprint.route("/url/<int:url_id>", methods=["DELETE"])
def delete_url(url_id):
    try:

        url_exists = db.url_exists("id", url_id)

        if url_exists:
            situation = 'URL_EXISTS'
        else:
            situation = 'URL_NOT_EXISTS'

        match situation:
            case 'URL_EXISTS':
                db.delete_url(url_id)
                return jsonify({"message": "Url deleted"}), 200
            case 'URL_NOT_EXISTS':
                message_error = {"message": "This URL doesnt exists"}
                return jsonify(message_error), 400

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400
