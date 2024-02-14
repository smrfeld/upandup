import upandup as upup
from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin
from loguru import logger

# First, define some dataclasses. 
# Let's say you have a `DataSchema` dataclass, which is the latest version, but also 2 older versions called `DataSchemaV1` and `DataSchemaV2`. 

@dataclass
class DataSchemaV1(DataClassJSONMixin):
    """First version of the data schema.
    """    
    x: int

@dataclass
class DataSchemaV2(DataClassJSONMixin):
    """Second version of the data schema.
    """    
    x: int
    y: int
    z: int = 0

@dataclass
class DataSchema(DataClassJSONMixin):
    """Latest version of the data schema.
    """    
    x: int
    name: str

# Define the functions to update between the versions
# The functions take the start and end classes, and the object to update
# The functions should return an object of the end class
# The functions can be lambdas or regular functions
# For the first update, we need to add a default value for the new field `y` (`z` already has a default).
update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)

# For the second update, we need to exclude the fields `y` and `z`, and add the new field `name` with a default value.
update_2_to_latest = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, name="default")

# Register the update under the label `DataSchema`
upup.register_updates("DataSchema", DataSchemaV1, DataSchemaV2, fn_update=update_1_to_2)
upup.register_updates("DataSchema", DataSchemaV2, DataSchema, fn_update=update_2_to_latest)

# Expose a helper function to load the latest version of the schema
load_data_schema = upup.make_load_fn("DataSchema")

# Load the latest version of the schema from any version
for i,fname in enumerate(["version_DataSchemaV1.json", "version_DataSchemaV2.json", "version_DataSchema.json"]):
    logger.info(f"--- Experiment {i}: Loading from file: {fname} ---")

    with open(fname, "r") as f:
        content = f.read()
        logger.info(f'Content of file: {content.__repr__()}')
        obj = load_data_schema(content, upup.LoadOptions())
        logger.info(f"After updating, loaded object: {obj} of type {type(obj).__name__}")