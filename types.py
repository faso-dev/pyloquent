from typing import TypeVar, Dict, Any, List, Optional, Union, Type, Callable
from datetime import datetime



ModelType = TypeVar('ModelType', bound='Any')

FilterValue = Union[str, int, float, bool, datetime, None]
FilterOperator = str
JsonDict = Dict[str, Any] 