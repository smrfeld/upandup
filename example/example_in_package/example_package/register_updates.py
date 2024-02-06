import upandup as upup
from example_package.data1 import DataSchema1
from example_package.data2 import DataSchema2
from example_package.data3 import DataSchema3

update_1_to_2 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, y=0)
update_2_to_3 = lambda cls_start, cls_end, obj_start: cls_end(x=obj_start.x, name="default")

# Register the update
upup.register_updates("DataSchema", DataSchema1, DataSchema2, fn_update=update_1_to_2)
upup.register_updates("DataSchema", DataSchema2, DataSchema3, fn_update=update_2_to_3)

# Expose the load function and options in a nicer way
load_data_schema = upup.make_load_fn("DataSchema")
Options = upup.Options