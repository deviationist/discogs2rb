import argparse
from typing import List
import os


def get_boolenv(key: str, default: bool | str) -> bool:
    return str_to_bool(os.getenv(key, default))


def str_to_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.lower() in ("1", "true", "yes", "on")


def parse_script_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity: -v = INFO, -vv = DEBUG",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the actions without making changes.",
    )

    return parser.parse_args()
