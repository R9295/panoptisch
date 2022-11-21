import importlib
from types import ModuleType


def import_module(module_name: str) -> ModuleType:
    return importlib.import_module(module_name)
