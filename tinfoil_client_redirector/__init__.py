from flask import Flask
from pathlib import Path


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        MONGO_URI="mongodb://localhost:27017/tinfoil_client_db",
    )

    app.config.from_json("config.json", silent=True)

    instance_path = Path(app.instance_path)
    if not instance_path.is_dir():
        instance_path.mkdir(parents=True)

    from . import db
    db.init_app(app)

    from . import redirector
    app.register_blueprint(redirector.redirector_bp)

    return app
