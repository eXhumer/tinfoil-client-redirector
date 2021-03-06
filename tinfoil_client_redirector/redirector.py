import json
from flask import Blueprint, request
from tinfoil_client_redirector.db import get_db
from tinfoil_client_redirector.utils import valid_tinfoil_request

redirector_bp = Blueprint("redirector", __name__)


@redirector_bp.route("/")
def redirector():
    if valid_tinfoil_request(get_db()):
        return json.dumps({"success": "Hello Tinfoil :)"})
    return f"<h1>Add {request.url_root} to Tinfoil to use!</h1>"
