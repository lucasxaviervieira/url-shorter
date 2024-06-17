from flask import Flask, jsonify, request
from db.pgsql import Database

app = Flask(__name__)

db = Database()
db.connect()
db.create_table()


@app.route("/", methods=["GET"])
def get_urls():
    urls = db.get_urls()
    return jsonify(urls)


@app.route("/", methods=["POST"])
def create_url():
    try:
        original_url = request.json["original_url"]
        shorter_url = request.json["shorter_url"]

        new_url = db.create_url(original_url, shorter_url)
        return jsonify(new_url), 201

    except:
        return "Error"


if __name__ == "__main__":
    app.run(debug=True)
