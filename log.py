from loguru import logger

logger.add('log/file_{time}.log', enqueue=True, rotation='100MB', encoding='utf-8')


def info(log):
    logger.info(log)


def debug(log):
    logger.debug(log)
