import upandup as upup
from dataclasses import dataclass
from mashumaro import DataClassDictMixin

# First, define some dataclasses. 
# Let's say you have a `DataSchema` dataclass, which is the latest version, but also 2 older versions called `DataSchemaV1` and `DataSchemaV2`. 
# These classes have `to_json` and `from_json` methods defined via the `mashumaro` package by inheriting from `DataClassDictMixin` (they could also be defined manually).

@dataclass
class DataSchemaV1(DataClassDictMixin):
    x: int

@dataclass
class DataSchemaV2(DataClassDictMixin):
    x: int
    y: int
    z: int = 0

@dataclass
class DataSchema(DataClassDictMixin):
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

# Test the update
data = {"x": 1}
obj = load_data_schema(data, upup.Options())

print("Result:")
print(f"Loaded object: {obj} of type {type(obj).__name__}") # Loaded object: DataSchema(x=1, name='default') of type DataSchema