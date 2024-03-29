from upandup.serializer import deserialize, serialize, write_obj
from dataclasses import dataclass
from typing import Callable, List, Optional, Any, Dict
from loguru import logger
import os
import json
from mashumaro import DataClassDictMixin


@dataclass
class UpdateInfo:
    """Update info for one step in the update process.
    """    

    label: str
    "Label for the schema."

    cls_start: type
    "Class to update from."

    cls_end: type
    "Class to update to."

    fn_update: Callable[[type,type,object], object]
    "Function to update from start to end class. Args: cls_start, cls_end, obj_start. Returns: obj_end."


class Updater:
    """Updater for a schema.
    """    

    def __init__(self, label: str):
        """Constructor.

        Args:
            label (str): Unique label for the schema.
        """        
        self.label = label
        self._updates: List[UpdateInfo] = []
    

    @property
    def no_update_steps(self) -> int:
        """Number of update steps.

        Returns:
            int: Number of update steps.
        """        
        return len(self._updates)


    @property
    def cls_list(self) -> List[type]:
        """List of classes involved in the update, in order.

        Returns:
            List[type]: List of classes involved in the update, in order.
        """        
        return [u.cls_start for u in self._updates] + [self._updates[-1].cls_end]


    def register_updates(self, 
        cls_start: type, 
        cls_end: type, 
        fn_update: Callable[[type,type,object], object]
        ):
        """Register an update step.

        Args:
            cls_start (type): Start class.
            cls_end (type): End class.
            fn_update (Callable[[type,type,object], object]): Function to update from start to end class. Args: cls_start, cls_end, obj_start. Returns: obj_end.
        """        
        if len(self._updates) > 0:

            # Check it's a one way
            assert cls_start == self._updates[-1].cls_end, f"Class mismatch - start class: {cls_start} of new update step does not match most recent end class: {self._updates[-1].cls_end}"

            # Check no loops
            assert cls_end not in self.cls_list, f"Loop detected: {cls_end} in {self.cls_list}"

        info = UpdateInfo(label=self.label, cls_start=cls_start, cls_end=cls_end, fn_update=fn_update)
        assert self._update_info_for_cls(info.cls_start) is None, f"Update already exists for start class: {info.cls_start}"
        self._updates.append(info)
        logger.debug(f"Registered update: {self.label} {cls_start.__name__} -> {cls_end.__name__}")


    def _update_info_for_obj(self, obj_start: object) -> Optional[UpdateInfo]:
        """Update info for an object.

        Args:
            obj_start (object): Object to update.

        Returns:
            Optional[UpdateInfo]: Update info for the object.
        """        
        return self._update_info_for_cls(type(obj_start))


    def _update_info_for_cls(self, cls_start: type) -> Optional[UpdateInfo]:
        """Update info for a class.

        Args:
            cls_start (type): Class to update from.

        Returns:
            Optional[UpdateInfo]: Update info for the class.
        """        
        updates_exist = [u for u in self._updates if u.cls_start == cls_start]
        return updates_exist[0] if len(updates_exist) else None


    @dataclass
    class Options(DataClassDictMixin):
        """Options for the updater.
        """        

        write_versions: bool = False
        "Flag to write versions. Default: False."

        write_versions_dir: str = "."
        "Directory to write versions. Only used if write_versions is True. Default: '.'."

        write_version_prefix: str = ""
        "Prefix for version files. Only used if write_versions is True. Default: ''."


    def _write_obj_if_needed(self, obj: object, options: Options):
        """Write object if needed.

        Args:
            obj (object): Object to write.
            options (Options): Options.
        """        
        if options.write_versions:
            cls_name = obj.__class__.__name__
            bname_wo_ext = f"{options.write_version_prefix}_{cls_name}" if options.write_version_prefix else cls_name
            write_obj(obj, options.write_versions_dir, bname_wo_ext)


    def update(self, obj_start: object, options: Options = Options()) -> object:
        """Update an object, if needed.

        Args:
            obj_start (object): Object to update.
            options (Options, optional): Options. Defaults to Options().

        Returns:
            object: Object after updating.
        """        
        # Write initial version if needed
        self._write_obj_if_needed(obj_start, options)

        info = self._update_info_for_obj(obj_start)
        while info:
            logger.debug(f"Updating {info.label} from {info.cls_start.__name__} to {info.cls_end.__name__}")
            obj_start = _update_step(obj_start, info)
            info = self._update_info_for_obj(obj_start)

            # Write versions if needed
            self._write_obj_if_needed(obj_start, options)
        
        return obj_start

# Global dictionary of updaters
updaters: Dict[str,Updater] = {}

def register_updates(
    label: str, 
    cls_start: type, 
    cls_end: type, 
    fn_update: Callable[[type,type,object], object]
    ):
    """Register an update step.

    Args:
        label (str): Unique label for the schema.
        cls_start (type): Class to update from.
        cls_end (type): Class to update to.
        fn_update (Callable[[type,type,object], object]): Function to update from start to end class. Args: cls_start, cls_end, obj_start. Returns: obj_end.
    """    
    updaters.setdefault(label, Updater(label)).register_updates(cls_start, cls_end, fn_update)


def _update_step(obj_start: object, info: UpdateInfo) -> object:
    """Update an object from one class to another.

    Args:
        obj_start (object): Object to update.
        info (UpdateInfo): Update info.

    Returns:
        object: Object after updating.
    """    
    cls_start = type(obj_start)
    assert cls_start == info.cls_start, f"Class mismatch: {cls_start} != {info.cls_start}"

    # Update
    return info.fn_update(cls_start, info.cls_end, obj_start)