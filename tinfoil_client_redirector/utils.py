from flask import request
from .db import get_db


def valid_tinfoil_request() -> bool:
    """Validate tinfoil requests with data from
    local mongodb connection.
    """
    db = get_db()
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
        valid_hauth = False
        valid_uauth = False

        hauth_key = request.url_root[:-0x1]
        uauth_key = request.url

        auth_query_filter = {"KEY": {"$in": [hauth_key, uauth_key]}}
        auth_infos = db.auth_collection.find(auth_query_filter)

        for auth_info in auth_infos:
            if auth_info:
                if auth_info["KEY"] == hauth_key:
                    valid_hauth = auth_info["VALUE"] == req_hauth
                elif auth_info["KEY"] == uauth_key:
                    valid_uauth = auth_info["VALUE"] == req_uauth

        return tinfoil_headers_present and valid_hauth and valid_uauth

    return False
