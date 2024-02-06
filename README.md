# Up-and-up

`upandup` is a simple schema versioning system for Python dataclasses.

## Example

```python
import upandup as upup
from dataclasses import dataclass
from mashumaro import DataClassDictMixin

@dataclass
class DataSchema1(DataClassDictMixin):
    x: int

@dataclass
class DataSchema2(DataClassDictMixin):
    x: int
    y: int
    z: int = 0

@dataclass
class DataSchema3(DataClassDictMixin):
    x: int
    name: str

def register_updates():
    update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)
    update_2_to_3 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, name="default")

    # Register the update
    upup.register_updates("DataSchema", DataSchema1, DataSchema2, fn_update=update_1_to_2)
    upup.register_updates("DataSchema", DataSchema2, DataSchema3, fn_update=update_2_to_3)
    return upup.make_load_fn("DataSchema")

# Register the updates
load_data_schema = register_updates()

# Test the update
data = {"x": 1}
obj = load_data_schema(data, upup.Options())
print(f"Loaded object of type DataSchema3: {obj}")
```