import logging

LOGGER = logging.getLogger("robot_router")
LOGGER.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)5s: %(message)s"))
LOGGER.addHandler(handler)
