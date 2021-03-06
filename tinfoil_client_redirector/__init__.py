from flask import Flask
from pathlib import Path


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        MONGO_URI="mongodb://localhost:27017/tinfoil_client_db",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    instance_path = Path(app.instance_path)
    if not instance_path.is_dir():
        instance_path.mkdir(parents=True)

    from . import db
    db.init_app(app)

    from . import redirector
    app.register_blueprint(redirector.redirector_bp)

    return app
