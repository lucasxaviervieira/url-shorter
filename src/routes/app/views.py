from flask import Blueprint, render_template


app_blueprint = Blueprint("app_view", __name__, template_folder="templates")


@app_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home/index.html")


@app_blueprint.route("/<int:link_id>", methods=["GET"])
def links(link_id):
    return render_template("link/index.html", link_id=link_id)
