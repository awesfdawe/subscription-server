import uvicorn

from backend.config import get_config
from backend.logging import setup_logging

if __name__ == "__main__":
    setup_logging()

    config = get_config()

    uvicorn.run("backend.app:app", host=config.app.bind, port=config.app.port, log_config=None, access_log=False)
