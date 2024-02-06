import upandup as upup
import example_package
from loguru import logger

data = {"x": 1}
obj = upup.load("DataScheme", data)
logger.info(f"Loaded object: {obj}")