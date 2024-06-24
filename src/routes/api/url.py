from flask import Blueprint, jsonify, request
from db.main import Url

url_blueprint = Blueprint(
    "url",
    __name__,
)   

class Situation:
    URL_EXISTS = 'URL_EXISTS'
    URL_NOT_EXISTS = 'URL_NOT_EXISTS'
    IS_NOT_URL = 'IS_NOT_URL'
    MAX_LENGTH = 'MAX_LENGTH'

@url_blueprint.route("/url/", methods=["GET"])
def get_urls():
    db = Url()
    db.start()
    urls = db.get_urls()
    db.disconnect()
    return jsonify(urls)


@url_blueprint.route("/url/<int:url_id>", methods=["GET"])
def get_url(url_id):
    try:
        db = Url()
        db.start()

        url_exists = db.url_exists("id", url_id)

        situation = Situation.URL_EXISTS if url_exists else Situation.URL_NOT_EXISTS

        match situation:
            case Situation.URL_EXISTS:
                url = db.get_url("id",url_id)
                db.disconnect()
                return jsonify(url), 200
            case Situation.URL_NOT_EXISTS:
                db.disconnect()
                message_error = {"message": "This URL doesnt exists"}
                return jsonify(message_error), 400


    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400


@url_blueprint.route("/url/", methods=["POST"])
def create_url():
    try:
        db = Url()
        db.start()

        original_url = request.json["original_url"]
                
        protocol, https = "https://", original_url[:8]
            
        is_url = True if https == protocol else False     
        
        url_exists = db.url_exists("original_url", original_url)
        
        decent_num_char = len(original_url) < 255
    
        situation = None
        
        if decent_num_char:
            if is_url:
                if url_exists:
                    situation = Situation.URL_EXISTS
                else:                    
                    situation = Situation.URL_NOT_EXISTS
            else:                
                situation = Situation.IS_NOT_URL
        else:
            situation = Situation.MAX_LENGTH
        
        match situation:
            case Situation.URL_EXISTS:
                url = db.get_url("original_url", original_url)
                db.disconnect()
                message = {"message":"This URL exists" , "data": url}
                return jsonify(message), 200
            case Situation.URL_NOT_EXISTS:
                new_url = db.create_url(original_url)
                db.disconnect()
                return jsonify(new_url), 200
            case Situation.IS_NOT_URL:
                db.disconnect()
                message_error = {"message": "This not longer an URL"}
                return jsonify(message_error), 400
            case Situation.MAX_LENGTH:
                db.disconnect()
                message_error = {"message": "Max 255 charapters"}
                return jsonify(message_error), 400         

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400


@url_blueprint.route("/url/<int:url_id>", methods=["DELETE"])
def delete_url(url_id):
    try:
        db = Url()
        db.start()

        url_exists = db.url_exists("id", url_id)
        
        situation = Situation.URL_EXISTS if url_exists else Situation.URL_NOT_EXISTS

        match situation:
            case Situation.URL_EXISTS:
                db.delete_url(url_id)
                db.disconnect()
                return jsonify({"message": "Url deleted"}), 200
            case Situation.URL_NOT_EXISTS:
                message_error = {"message": "This URL doesnt exists"}
                db.disconnect()
                return jsonify(message_error), 400

    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400
