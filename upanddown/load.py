from updanddown.checker import Serializer, check_serializer, serialize_obj
from dataclasses import dataclass
from typing import Callable, List, Optional

@dataclass
class UpdateInfo:
    cls_start: type
    cls_end: type
    fn_update: Callable[[type,type,object], object]

updates: List[UpdateInfo] = []

def _update_info_for_obj(obj_start: object) -> Optional[UpdateInfo]:
    return _update_info_for_cls(type(obj_start))

def _update_info_for_cls(cls_start: type) -> Optional[UpdateInfo]:
    updates_exist = [u for u in updates if u.cls_start == cls_start]
    return updates_exist[0] if len(updates_exist) else None

def register_updates(info: UpdateInfo):
    assert _update_info_for_cls(info.cls_start) is None, f"Update already exists for start class: {info.cls_start}"
    updates.append(info)

@dataclass
class Options:
    pass

def update(obj_start: object, options: Options) -> object:
    info = _update_info_for_obj(obj_start)
    while info:
        obj_start = _update_step(obj_start, info)
        info = _update_info_for_obj(obj_start)

    return obj_start

def _update_step(obj_start: object, info: UpdateInfo) -> object:
    cls_start = type(obj_start)
    assert cls_start == info.cls_start, f"Class mismatch: {cls_start} != {info.cls_start}"

    # Update
    return info.fn_update(cls_start, info.cls_end, obj_start)