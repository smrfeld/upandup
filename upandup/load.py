from upandup.checker import deserialize
from upandup.updater import Updater, updaters
from typing import Callable, List, Optional, Any, Dict
from loguru import logger

def load(label: str, data: Any) -> object:

    # Try to load classes in reverse order
    assert label in updaters, f"No updates registered for label: {label}"
    updater = updaters[label]
    assert updater.no_update_steps > 0, f"No updates registered for label: {label}"
    
    # Classes to check to deserialize
    cls_list = updater.cls_list

    # Try to deserialize, using most recent class first
    obj = None
    while obj is None and len(cls_list) > 0:
        cls = cls_list.pop()
        try:
            obj = deserialize(data, cls)
        except:
            continue
    
    # If no class worked, raise error
    assert obj is not None, f"Could not deserialize data with any class in {cls_list}"

    # Check if last class is the most recent
    if type(obj) != updater.cls_list[-1]:

        # Update
        obj = updater.update(obj, Updater.Options())
    
    return obj

def make_load_fn(label: str) -> Callable[[Any], object]:
    def load_fn(data: Any) -> object:
        return load(label, data)
    return load_fn