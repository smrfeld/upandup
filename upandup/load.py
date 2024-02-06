from upandup.serializer import deserialize
from upandup.updater import Updater, updaters
from typing import Callable, List, Optional, Any, Dict
from loguru import logger
from dataclasses import dataclass
from mashumaro import DataClassDictMixin


@dataclass
class Options(DataClassDictMixin):
    write_versions: bool = False
    write_versions_dir: str = "."
    write_version_prefix: str = ""


def load(label: str, data: Any, options: Options = Options()) -> object:

    # Convert to options
    options_updater = Updater.Options.from_dict(options.to_dict())

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
        except Exception as e:
            logger.debug(f"Could not deserialize data [{data}] with class {cls}: {e}")
            continue
    
    # If no class worked, raise error
    assert obj is not None, f"Could not deserialize data [{data}] with any class in {updater.cls_list}"

    # Check if last class is the most recent
    if type(obj) != updater.cls_list[-1]:

        # Update
        obj = updater.update(obj, options=options_updater)
    
    return obj

def make_load_fn(label: str) -> Callable[[Any, Options], object]:
    def load_fn(data: Any, options: Options = Options()) -> object:
        return load(label, data, options=options)
    return load_fn