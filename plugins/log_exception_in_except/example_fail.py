try:
    1 / 0
except ZeroDivisionError:
    # Плохо: error вместо exception в блоке except
    logger.error("Error occurred")
    log.critical("Critical fail")
    logger.warning("Warning")
