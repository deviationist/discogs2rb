import os
import argparse
from typing import List

_args: argparse.Namespace | None = None


def parse_script_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity: -v = INFO, -vv = DEBUG",
    )

    args = parser.parse_args()
    set_args(args)

    return args


def set_args(args: argparse.Namespace) -> None:
    global _args
    _args = args


def get_args() -> argparse.Namespace:
    if _args is None:
        raise RuntimeError("Arguments have not been initialized")
    return _args


def get_folders_to_ignore() -> List[str]:
    FOLDER_PATHS_TO_IGNORE = os.getenv("FOLDER_PATHS_TO_IGNORE")
    if not FOLDER_PATHS_TO_IGNORE:
        return []
    return [item.strip() for item in FOLDER_PATHS_TO_IGNORE.split(",")]


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
