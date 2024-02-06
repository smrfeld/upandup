import upanddown as updn
import example_package
from loguru import logger

data = {"x": 1}
obj = updn.load("DataScheme", data)
logger.info(f"Loaded object: {obj}")