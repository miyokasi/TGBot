import os

import logging
from dotenv import load_dotenv

from colorlog import ColoredFormatter

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)


console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


logger = logging.getLogger("resume_bot")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.propagate = False