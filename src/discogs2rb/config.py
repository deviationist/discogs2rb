import os
import argparse
from typing import Optional

_args: argparse.Namespace | None = None


def set_args(args: argparse.Namespace) -> None:
    global _args
    _args = args


def get_args() -> argparse.Namespace:
    if _args is None:
        raise RuntimeError("Arguments have not been initialized")
    return _args


def get_discogs_token() -> str:
    DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN")
    if not DISCOGS_TOKEN:
        raise Exception("Env DISCOGS_TOKEN missing")
    return DISCOGS_TOKEN


def get_various_artist_name() -> str:
    DISCOGS_TOKEN = os.getenv("VARIOUS_ARTIST_NAME")
    if not DISCOGS_TOKEN:
        raise Exception("Env VARIOUS_ARTIST_NAME missing")
    return DISCOGS_TOKEN


def get_logger_name() -> str:
    LOGGER_NAME = os.getenv("LOGGER_NAME")
    if LOGGER_NAME:
        return LOGGER_NAME
    return "discogs2rb"

def get_db_path() -> str:
    DB_PATH = os.getenv("REKORDBOX_MASTERDB_PATH")
    if not DB_PATH:
        raise Exception("Env REKORDBOX_MASTERDB_PATH missing")
    return DB_PATH


def get_db_pass() -> str:
    DB_PASSWORD = os.getenv("REKORDBOX_MASTERDB_PASSWORD")
    if not DB_PASSWORD:
        raise Exception("Env REKORDBOX_MASTERDB_PASSWORD missing")
    return DB_PASSWORD
