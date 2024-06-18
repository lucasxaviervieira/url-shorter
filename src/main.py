from flask import Flask
from routes.api.url import url_blueprint
from routes.app.views import app_blueprint

app = Flask(__name__)

app.register_blueprint(url_blueprint, url_prefix="/api")
app.register_blueprint(app_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
