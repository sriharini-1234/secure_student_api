# import logging
# from pathlib import Path


# BASE_DIR = Path(__file__).resolve().parent.parent

# LOG_DIR = BASE_DIR / "logs"
# LOG_DIR.mkdir(parents=True, exist_ok=True)

# LOG_FILE = LOG_DIR / "app.log"


# logger = logging.getLogger("secure_student_api")
# logger.setLevel(logging.INFO)

# file_handler = logging.FileHandler(LOG_FILE)

# formatter = logging.Formatter(
#     "%(asctime)s - %(levelname)s - %(message)s"
# )

# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)

import logging
import sys

logger = logging.getLogger("secure_student_api")
logger.setLevel(logging.INFO)
logger.propagate = False

# Avoid adding duplicate handlers
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
