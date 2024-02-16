---
title: "UpAndUp Documentation"
showToc: true
---

`upandup` is a simple schema versioning system for Python dataclasses.

Contents:
* [Why?](#why)
* [Serialization formats supported](#serialization-formats-supported)

## Why UpAndUp?

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

