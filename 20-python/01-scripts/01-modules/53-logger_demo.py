import logging
import logging.config

logger_conf = {
    "version": 1,
    "formatters": {
        "precise": {
            "format": "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s",
            "datefmt": f"%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "formatter": "precise",
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "precise",
            "filename": "server_werkzeug.log",
            "maxBytes": 1024 * 1024,
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {  # root logger
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
        "werkzeug": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
    },
}

# Run once at startup:
logging.config.dictConfig(logger_conf)

# Include in each module:
log = logging.getLogger(__name__)
log.debug("Logging is configured.")


# config by basic
logging.basicConfig(
    format="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    # handlers=[logging.StreamHandler()]
)
logger = logging.getLogger()
logging.info('init')
