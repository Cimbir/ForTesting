from finalproject.api.api import RunFastAPIUsingUvicorn
from finalproject.runner.setup import setup

DEFAULT_PORT = 9000

if __name__ == "__main__":
    setup(RunFastAPIUsingUvicorn(port=DEFAULT_PORT)).run_app()
