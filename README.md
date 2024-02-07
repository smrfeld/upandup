# Up-and-up :rocket:

`upandup` is a simple schema versioning system for Python dataclasses.

## Why?

In Python, `dataclasses` are a great way to define data schemas. However, when the schema changes, you need to be able to update the old data to the latest version, or risk breaking the ability to load old data from JSON, YAML, or other formats.

`upandup` provides a simple way to define how to update between different versions of a schema, and then load the latest version of the schema from old data.

Let's say you have a `dataclass` like this:

```python
@dataclass
class DataSchemaV1:
    x: int
```

Users might end up serializing this to JSON:

```json
{
    "x": 1
}
```

Later, you decide to add a new field `y`:

```python
@dataclass
class DataSchema:
    x: int
    x_str: str
```

Now, users can no longer load the old data, because the schema has changed. You need to define how to update the old data to the new schema. `upandup` provides a way to do this. 

```python
import upandup as upup

update = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, x_str="the value is: %d" % obj_start.x)

# Register the update
upup.register_updates("DataSchema", DataSchemaV1, DataSchema, fn_update=update)
```

In the end, `upandup` exposes a `load` method that users can call to load the latest version of the schema from old data **every time**.

```python
data = { x: 1 }
obj = upup.load("DataSchema", data)
print(obj.x_str) # the value is: 1
```

This `load` method can also be exposed as an anonymous function such as:

```python
# In your package:
load_data_schema = upup.make_load_fn("DataSchema")

# In scripts using your package
data = { x: 1 }
obj = load_data_schema(data)
```

## Serialization formats supported

* Dictionary - define `to_dict` and `from_dict` methods on your dataclasses.
* JSON - define `to_json` and `from_json` methods on your dataclasses.
* YAML - define `to_yaml` and `from_yaml` methods on your dataclasses.
* TOML - define `to_toml` and `from_toml` methods on your dataclasses.

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
obj = load_data_schema(data, options=upup.LoadOptions())

print("Result:")
print(f"Loaded object: {obj} of type {type(obj)}") # Loaded object: DataSchema(x=1, name='default') of type DataSchema
```

## Advanced

### Write intermediate versions

By default, the intermediate versions from updating to the latest are not written to the output. If you want to write them, you can set the `write_intermediate` option to `True`.

```python
data = {"x": 1}
options = upup.LoadOptions(write_versions=True, write_version_prefix="version", write_versions_dir=".")
obj = upup.load("DataSchema", data, options=options)
```

This will write the files:
```
version_DataSchema.json
version_DataSchemaV1.json
version_DataSchemaV2.json
```

### Example in a package

We can organize the same example above to demonstrate how to use it in a package.

Create the following files:

```
setup.py
mypackage/
    __init__.py
    data_latest.py
    data_v1.py
    data_v2.py
    register_updates.py
run_example.py
```

The data schemas are defined by `data_v1.py`, `data_v2.py`, and `data_latest.py`. The update functions between them are defined in `register_updates.py`.

The package is installed by the `setup.py` file:

```python
from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.1.0',
    description='An example package',
    packages=find_packages(),
    install_requires=[
        "loguru",
        "mashumaro",
        "setuptools",
        "upandup"
    ],
    python_requires='>=3.11',
)
```

The contents of `data_v1.py` are:

```python
from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchemaV1(DataClassDictMixin):
    x: int
```

The contents of `data_v2.py` are:

```python
from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchemaV2(DataClassDictMixin):
    x: int
    y: int
    z: int = 0
```

The contents of `data_latest.py` are:

```python
from mashumaro import DataClassDictMixin
from dataclasses import dataclass

@dataclass
class DataSchema(DataClassDictMixin):
    x: int
    name: str
```

The `__init__.py` exposes only the latest version of the schema:

```python
from .data_latest import DataSchema
from .register_updates import load_data_schema, Options
```

The `register_updates.py` contains the update functions:

```python
import upandup as upup
from mypackage.data_v1 import DataSchemaV1
from mypackage.data_v2 import DataSchemaV2
from mypackage.data_latest import DataSchema

update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)
update_2_to_latest = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, name="default")

# Register the update
upup.register_updates("DataSchema", DataSchemaV1, DataSchemaV2, fn_update=update_1_to_2)
upup.register_updates("DataSchema", DataSchemaV2, DataSchema, fn_update=update_2_to_latest)

# Expose the load function and options in a nicer way
load_data_schema = upup.make_load_fn("DataSchema")
Options = upup.LoadOptions
```

As noted in the `__init__.py`, we also expose the `load_data_schema` and `Options` from `register_updates.py`. This lets users easily load the latest version of the schema **every time** from any old version.

Finally, the `run_example.py` contains the test code:

```python
import mypackage as mp

# Test the update
data = {"x": 1}
obj = mp.load_data_schema(data, mp.Options())
print("Result:")
print(f"Loaded object: {obj} of type {type(obj).__name__}") # Loaded object: DataSchema(x=1, name='default') of type DataSchema
```

Note that the `upandup` package itself did not have to be called.

### Tests

Tests are included in the `tests` directory and built on `pytest` - from the root directory, run:

```bash
pytest
```