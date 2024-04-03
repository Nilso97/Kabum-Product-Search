from flask import Flask
from dotenv import load_dotenv
from src.config.config import config
from src.config.cache.cache import cache
from src.database.DatabaseContext import db
from src.routes.routes import consult_blueprint

load_dotenv(".env")

app = Flask(__name__, template_folder="templates")

app.register_blueprint(blueprint=consult_blueprint)

app.config.from_mapping(config)

cache.init_app(app, config)

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=True)
