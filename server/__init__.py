import json
import logging.config
import os
from dotenv import load_dotenv
from flask import Flask
from raven.conf import setup_logging
from raven.contrib.flask import Sentry
from raven.handlers.logging import SentryHandler
import mediacloud.api

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# setup logging
with open(os.path.join(base_dir, 'config', 'server-logging.json'), 'r') as f:
    logging_config = json.load(f)
    logging_config['handlers']['file']['filename'] = os.path.join(base_dir,
                                                                  logging_config['handlers']['file']['filename'])
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)
logger.info("---------------------------------------------------------------------------")

# load the env vars
load_dotenv()

MC_API_KEY = os.environ.get('MC_API_KEY', None)
CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL', None)
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', None)
TWITTER_API_BEARER_TOKEN = os.environ.get('TWITTER_API_BEARER_TOKEN', None)

# setup optional sentry logging service
if SENTRY_DSN is not None:
    sentry_handler = SentryHandler(SENTRY_DSN)
    sentry_handler.setLevel(logging.ERROR)
    setup_logging(sentry_handler)
else:
    logger.info("no sentry logging")


mc = mediacloud.api.AdminMediaCloud(MC_API_KEY)
logger.info("Connected to mediacloud")


def create_app():
    # Factory method to create the app
    my_app = Flask(__name__)
    if SENTRY_DSN is not None:
        Sentry(my_app, dsn=SENTRY_DSN)
    return my_app


app = create_app()

import server.api
