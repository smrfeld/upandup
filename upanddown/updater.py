from upanddown.checker import deserialize
from dataclasses import dataclass
from typing import Callable, List, Optional, Any, Dict
from loguru import logger

@dataclass
class UpdateInfo:
    label: str
    cls_start: type
    cls_end: type
    fn_update: Callable[[type,type,object], object]

class Updater:

    def __init__(self, label: str):
        self.label = label
        self._updates: List[UpdateInfo] = []
    
    @property
    def no_update_steps(self) -> int:
        return len(self._updates)

    @property
    def cls_list(self) -> List[type]:
        return [u.cls_start for u in self._updates] + [self._updates[-1].cls_end]

    def register_updates(self, 
        cls_start: type, 
        cls_end: type, 
        fn_update: Callable[[type,type,object], object]
        ):
        if len(self._updates) > 0:

            # Check it's a one way
            assert cls_start == self._updates[-1].cls_end, f"Class mismatch: {cls_start} != {self._updates[-1].cls_end}"

            # Check no loops
            assert cls_end not in self.cls_list, f"Loop detected: {cls_end} in {self.cls_list}"

        info = UpdateInfo(label=self.label, cls_start=cls_start, cls_end=cls_end, fn_update=fn_update)
        assert self._update_info_for_cls(info.cls_start) is None, f"Update already exists for start class: {info.cls_start}"
        self._updates.append(info)
        logger.debug(f"Registered update: {self.label} {cls_start} -> {cls_end}")

    def _update_info_for_obj(self, obj_start: object) -> Optional[UpdateInfo]:
        return self._update_info_for_cls(type(obj_start))

    def _update_info_for_cls(self, cls_start: type) -> Optional[UpdateInfo]:
        updates_exist = [u for u in self._updates if u.cls_start == cls_start]
        return updates_exist[0] if len(updates_exist) else None

    @dataclass
    class Options:
        pass

    def update(self, obj_start: object, options: Options) -> object:
        info = self._update_info_for_obj(obj_start)
        while info:
            obj_start = _update_step(obj_start, info)
            info = self._update_info_for_obj(obj_start)

        return obj_start

updaters: Dict[str,Updater] = {}

def register_updates(
    label: str, 
    cls_start: type, 
    cls_end: type, 
    fn_update: Callable[[type,type,object], object]
    ):
    updaters.setdefault(label, Updater(label)).register_updates(cls_start, cls_end, fn_update)

def _update_step(obj_start: object, info: UpdateInfo) -> object:
    cls_start = type(obj_start)
    assert cls_start == info.cls_start, f"Class mismatch: {cls_start} != {info.cls_start}"

    # Update
    return info.fn_update(cls_start, info.cls_end, obj_start)