from upanddown.checker import deserialize
from dataclasses import dataclass
from typing import Callable, List, Optional, Any, Dict

@dataclass
class UpdateInfo:
    label: str
    cls_start: type
    cls_end: type
    fn_update: Callable[[type,type,object], object]

updates: Dict[str,List[UpdateInfo]] = {}

def _update_info_for_obj(label: str, obj_start: object) -> Optional[UpdateInfo]:
    return _update_info_for_cls(label, type(obj_start))

def _update_info_for_cls(label: str, cls_start: type) -> Optional[UpdateInfo]:
    updates_exist = [u for u in updates.get(label,[]) if u.cls_start == cls_start]
    return updates_exist[0] if len(updates_exist) else None

def register_updates(label: str, cls_start: type, cls_end: type, fn_update: Callable[[type,type,object], object]):
    info = UpdateInfo(label=label, cls_start=cls_start, cls_end=cls_end, fn_update=fn_update)
    assert _update_info_for_cls(label, info.cls_start) is None, f"Update already exists for start class: {info.cls_start}"
    updates.setdefault(label,[]).append(info)
    print(f"Registered update: {label} {cls_start} -> {cls_end}")

@dataclass
class Options:
    pass

def update(label: str, obj_start: object, options: Options) -> object:
    info = _update_info_for_obj(label, obj_start)
    while info:
        obj_start = _update_step(obj_start, info)
        info = _update_info_for_obj(label, obj_start)

    return obj_start

def _update_step(obj_start: object, info: UpdateInfo) -> object:
    cls_start = type(obj_start)
    assert cls_start == info.cls_start, f"Class mismatch: {cls_start} != {info.cls_start}"

    # Update
    return info.fn_update(cls_start, info.cls_end, obj_start)

def load(label: str, data: Any) -> object:

    # Try to load classes in reverse order
    updates_for_label = updates.get(label,[])
    assert len(updates_for_label) > 0, f"No updates found for label: {label}"

    # Classes to check to deserialize
    cls_list = [updates_for_label[0].cls_start] + [u.cls_end for u in updates_for_label]

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
    if type(obj) != updates_for_label[0].cls_end:

        # Update
        print(f"Updating {label} from {type(obj)} to {updates_for_label[0].cls_end}")
        obj = update(label, obj, Options())

    return obj