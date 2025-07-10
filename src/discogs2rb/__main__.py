import dotenv
from . import config
from .rekordbox.RekordboxDB import setup_db_connection
from .utils.logger import init_logger
from .actions.ResolveDiscogsTracks import ResolveDiscogsTracks

dotenv.load_dotenv()


def main():
    args = config.parse_script_arguments()
    init_logger(args)
    setup_db_connection()
    ResolveDiscogsTracks().exec()
