from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
    _utils
)

from loguru import logger


def after_log(logger, log_level):
    """After call strategy that logs to some logger the finished attempt."""

    def log_it(retry_state):
        logger.log(
            log_level,
            "Call '{0}' after {1:.3f}(s), {2} time. Error log: '{3}'".format(
                _utils.get_callback_name(retry_state.fn),
                retry_state.seconds_since_start,
                _utils.to_ordinal(retry_state.attempt_number),
                repr(retry_state.outcome.exception())
            ),
        )

    return log_it


@retry(
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    after=after_log(logger, 'DEBUG'),
    reraise=True,
)
def callback_udf():
    raise Exception('eeeeeeeeeee')


if __name__ == '__main__':
    callback_udf()
