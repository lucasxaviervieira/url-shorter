from flask import Blueprint, render_template


app_blueprint = Blueprint("app_view", __name__, template_folder="templates")


@app_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home/index.html")
