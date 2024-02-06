import example_package as ep
from loguru import logger

data = {"x": 1}
obj = ep.load_data_schema(data)
logger.info(f"Loaded object: {obj}")