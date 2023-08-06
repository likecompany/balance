from __future__ import annotations

import uvicorn

from core.settings import server_settings
from logger import logger


def main() -> None:
    logger.info("Starting application. Uvicorn running")

    uvicorn.run(
        app="app:app",
        host=server_settings.HOSTNAME,
        port=server_settings.PORT,
        reload=server_settings.RELOAD,
    )


if __name__ == "__main__":
    main()
