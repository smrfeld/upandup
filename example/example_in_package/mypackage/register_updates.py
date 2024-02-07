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