from flask import Blueprint, request
from tinfoil_client_redirector.utils import (
    valid_tinfoil_request, get_user_redirector_index
)
redirector_bp = Blueprint("redirector", __name__)


@redirector_bp.route("/")
def redirector():
    if valid_tinfoil_request():
        return get_user_redirector_index()
    return f"<h1>Add {request.url_root} to Tinfoil to use!</h1>"
