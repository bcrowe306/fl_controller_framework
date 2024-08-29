from dataclasses import dataclass
from fl_controller_framework.util.enum import Enum

class PluginParameterType(Enum):
    Plugin = 0
    Channel = 1


class PluginParameter:

    def __init__(self,
        index: int = 0,
        name: str = "",
        value: float = 0.0,
        parameter_type = PluginParameterType.Plugin,
        deadzone_centre = None,
        deadzone_width = 0.1,
        discrete_regions = [],
                 ) -> None:
        self.index: int = index
        self.name: str = name
        self.value: float = value
        self.parameter_type =parameter_type
        self.deadzone_centre = deadzone_centre
        self.deadzone_width = deadzone_width
        self.discrete_regions = discrete_regions

    def __str__(self) -> str:
        return f"PluginParameter: index: {self.index}, name: {self.name}, parameter_type: {self.parameter_type}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
