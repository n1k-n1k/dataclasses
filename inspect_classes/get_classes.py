import sys
import inspect
import importlib.util

from typing import Dict

from pathlib import Path

from utils import get_traceback


class Passed:
    pass


def get_module_classes(path: str, parent_clz_name: str | None = None):
    _path = Path(path)
    python_files = [file_path for file_path in _path.glob("**/*") if str(file_path).endswith(".py")]
    _classes = {}
    for file_path in python_files:
        try:
            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            all_classes = {name: clz for name, clz in inspect.getmembers(module, inspect.isclass)}
            # pass imported classes
            module_classes = {name: clz for name, clz in all_classes.items() if module.__name__ == clz.__module__}

            if not parent_clz_name:
                _classes.update(module_classes)
            else:
                for name, clz in module_classes.items():
                    if name == parent_clz_name:  # pass parent class
                        continue
                    mro_classnames = [mro_cls.__name__ for mro_cls in inspect.getmro(clz)]
                    if parent_clz_name in mro_classnames:
                        _classes[name] = clz

        except Exception as ex:
            print(f"Parse classes error: `{ex}`")
            print(f"Traceback (most recent call last):\n{get_traceback(ex)}")
    return _classes


if __name__ == '__main__':
    from devtools import debug

    _path = str(Path(__file__).parent)
    print(_path)
    debug(get_module_classes(_path, 'ABCSuperPet'))
    debug(get_module_classes(_path))
