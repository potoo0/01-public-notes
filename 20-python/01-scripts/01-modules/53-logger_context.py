#!/usr/bin/env python3
from __future__ import annotations

# %% built-in logging
import logging
from contextvars import ContextVar

_log_cxt = ContextVar('log-context')


class ThreadingLocalContextFilter(logging.Filter):
    """injects context from `ContextVar` (_log_cxt) into the log."""
    def __init__(self, attributes: list[str]):
        super().__init__()
        self.attributes = attributes

    def filter(self, record) -> bool:
        context = _log_cxt.get(None) or {}
        for attr in self.attributes:
            setattr(record, attr, context.get(attr, '--'))
        return True


class SessionContext(object):
    def __init__(self, context: dict = None):
        self.context: dict = context
        self.tokens = []

    def __enter__(self):
        if self.context:
            self.tokens.append(_log_cxt.set(self.context))
        return self

    def __exit__(self, et, ev, tb):
        if self.tokens:
            _log_cxt.reset(self.tokens.pop())


logging.basicConfig(
    format="%(tid)s | %(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    # handlers=[logging.StreamHandler()]
)

logger = logging.getLogger('test-log-with-trace')
logger.addFilter(ThreadingLocalContextFilter(['tid']))
logger.info('logger with extra param', extra={'tid': 't1'})

with SessionContext(context={'tid': 'lv1'}):
    logger.info('logger inner 1')
    with SessionContext(context={'tid': 'lv2'}):
        logger.info('logger inner 2')
    logger.info('logger inner 1')


logger.info('logger outer')


# %% loguru
import sys  # noqa: E402

from loguru import logger as log  # noqa: E402

fmt = "extra_dict={extra} | extra_elem={extra[tid]} | {time:YYYY-MM-DDTHH:mm:ss} | {level: <5} | {name: ^15} | {function: ^15} | {line: >3} | {message}"
# # simple way, without extra default value
# log.remove()
# log.add(sys.stderr, format=fmt)

# config extra default value
config = {
    "handlers": [{"sink": sys.stdout, "format": fmt}],
    "extra": {'tid': '--'}
}
log.configure(**config)

with log.contextualize(tid='1'):
    log.info("End of task")
log.info("Out of task")

# %%
