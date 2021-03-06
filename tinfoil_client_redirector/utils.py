from flask_pymongo import PyMongo
from flask import request


def valid_tinfoil_request(mongo: PyMongo) -> bool:
    """Validate tinfoil requests with data from
    local mongodb connection.
    """
    req_hauth = request.headers.get("HAUTH")
    req_uauth = request.headers.get("UAUTH")
    req_theme = request.headers.get("Theme")
    req_uid = request.headers.get("UID")
    req_language = request.headers.get("Language")
    req_version = request.headers.get("Version")

    tinfoil_headers_present = bool(req_hauth and len(req_hauth) == 32)
    tinfoil_headers_present &= bool(req_uauth and len(req_uauth) == 32)
    tinfoil_headers_present &= bool(req_theme and len(req_theme) == 64)
    tinfoil_headers_present &= bool(req_uid and len(req_uid) == 64)
    tinfoil_headers_present &= bool(req_language and req_version)

    if tinfoil_headers_present:
        hauth_info = mongo.db.auth_collection.find_one({
            "AUTH_KEY": request.url_root[:-0x1],
        })
        uauth_info = mongo.db.auth_collection.find_one({
            "AUTH_KEY": request.url,
        })

        valid_hauth = bool(hauth_info and hauth_info["AUTH_VALUE"] ==
                           req_hauth)
        valid_uauth = bool(uauth_info and uauth_info["AUTH_VALUE"] ==
                           req_uauth)

        return tinfoil_headers_present and valid_hauth and valid_uauth

    return False
