from finalproject.api.api import RunFastAPIUsingUvicorn
from finalproject.runner.setup import setup

DEFAULT_PORT = 9000
PERSISTENT_DATABASE_PATH = "pos.db"

if __name__ == "__main__":
    setup(
        RunFastAPIUsingUvicorn(port=DEFAULT_PORT), database=PERSISTENT_DATABASE_PATH
    ).run_app()
