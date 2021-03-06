from typing import List
import click
from flask import current_app, g
from flask_pymongo import PyMongo
from flask.cli import with_appcontext
from pymongo.database import Database


def get_db() -> Database:
    if "db" not in g:
        g.db = PyMongo(current_app).db

    assert isinstance(g.db, Database)
    return g.db


def close_db(e=None):
    if "db" in g:
        assert isinstance(g.pop("db"), Database)


def init_db():
    pass


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


@click.command("import-auth-value")
@click.argument("key", nargs=1)
@click.argument("value", nargs=1)
@with_appcontext
def import_auth_value_command(key: str, value: str):
    db = get_db()
    check_existing_key = db.auth_collection.find_one({
        "KEY": key,
    })
    if check_existing_key:
        if check_existing_key["VALUE"] != value:
            click.echo("Key found in database, but different value " +
                       "specified. Updating value!")
            db.auth_collection.update_one(
                check_existing_key,
                {"$set": {
                    "VALUE": value,
                }},
            )
    else:
        click.echo("Key doesn't exist in database, adding it!")
        db.auth_collection.insert_one({
            "KEY": key,
            "VALUE": value,
        })


@click.command("blacklist-uid")
@click.argument("uids", nargs=-1)
@click.argument("reason", nargs=1)
@with_appcontext
def blacklist_uid(uids: List[str], reason: str):
    db = get_db()

    uids_query_filter = {"UID": {"$in": uids}}
    already_blacklisted_users = db.blacklist_collection.find(
        uids_query_filter,
    )

    for blacklisted_user in already_blacklisted_users:
        blacklist_uid = blacklisted_user["UID"]
        blacklist_reason = blacklisted_user["REASON"]
        click.echo(f"UID {blacklist_uid} already blacklisted!\n" +
                   f"Reason: {blacklist_reason}")
        uids.remove(blacklist_uid)

    if len(uids):
        result = db.blacklist_collection.insert_many([
            {"UID": uid, "REASON": reason} for uid in uids
        ])
        click.echo(result.inserted_ids)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(blacklist_uid)
    app.cli.add_command(init_db_command)
    app.cli.add_command(import_auth_value_command)
