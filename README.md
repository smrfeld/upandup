# Up-and-up

`upandup` is a simple schema versioning system for Python dataclasses.

## Example

First, define some dataclasses. Let's say you have a `DataSchema` dataclass, which is the latest version, but also 2 older versions called `DataSchemaV1` and `DataSchemaV2`. These classes have `to_json` and `from_json` methods defined via the `mashumaro` package by inheriting from `DataClassDictMixin` (they could also be defined manually).

```python
from dataclasses import dataclass
from mashumaro import DataClassDictMixin

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
```

Here, the first version `DataSchemaV1` has only one field `x`, and the second version `DataSchemaV2` has 3 fields `x`, `y`, and `z`. The field `y` has no default, so we will have to define how to update it. The field `z` already has a default in the definition. In the final version, the fields `y` and `z` have been removed again, and a new field `name` has been added.

Now, we can define how to update between the versions. We can use the `upandup` package to do this.

```python
import upandup as upup

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
# This makes a thin wrapper around upup.load
load_data_schema = upup.make_load_fn("DataSchema")
```

Finally, we can test the update.

```python
# Test the update
data = {"x": 1}
obj = load_data_schema(data, options=upup.Options())

print("Result:")
print(f"Loaded object: {obj} of type {type(obj)}") # Loaded object: DataSchema(x=1, name='default') of type DataSchema
```

## Options

### Write intermediate versions

By default, the intermediate versions from updating to the latest are not written to the output. If you want to write them, you can set the `write_intermediate` option to `True`.

```python
data = {"x": 1}
options = upup.Options(write_versions=True, write_version_prefix="output", write_versions_dir=".")
obj = upup.load("DataSchema", data, options=options)
```

This will write the files:
```
output_
```