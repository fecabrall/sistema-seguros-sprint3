import logging, os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
load_dotenv()

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

def get_logger(name='neoroute'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        fmt = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
        ch = logging.StreamHandler(); ch.setFormatter(fmt); logger.addHandler(ch)
        fh = RotatingFileHandler(LOG_FILE, maxBytes=10_000_000, backupCount=5, encoding='utf-8'); fh.setFormatter(fmt); logger.addHandler(fh)
    return logger
