""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

https://github.com/mdklatt/cookiecutter-python-app
"""
from os import PathLike
import re

from pathlib import Path
from string import Template
from typing import Any, Mapping, Sequence

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib


from .logger import logger


__all__ = ["config", "TomlConfig"]


class _AttrDict(dict):
    """ A dict-like object with attribute access.

    """
    def __getitem__(self, key:str) -> Any:
        """ Access dict values by key.

        :param key: key to retrieve
        :type key: str
        :return: The value as _AttrDict at key
        :rtype: Any
        """
        value = super().__getitem__(key)
        if isinstance(value, dict):
            # For mixed recursive assignment (e.g. `a["b"].c = value` to work
            # as expected, all dict-like values must themselves be _AttrDicts.
            # The "right way" to do this would be to convert to an _AttrDict on
            # assignment, but that requires overriding both __setitem__
            # (straightforward) and __init__ (good luck). An explicit type
            # check is used here instead of EAFP because exceptions would be
            # frequent for hierarchical data with lots of nested dicts.
            self[key] = value = _AttrDict(value)
        return value

    def __getattr__(self, key:str) -> Any:
        """ Get dict values as attributes.

        :param key: key to retrieve
        :type key: str
        :return: The value as exists at key
        :rtype: Any
        """
        return self[key]

    def __setattr__(self, key:str, value:Any) -> None:
        """ Set dict values as attributes.

        :param key: key to set
        :type key: str
        :param value: new value for key
        :type value: Any
        """
        self[key] = value


class TomlConfig(_AttrDict):
    """ Store data from TOML configuration files.

    """
    def __init__(
        self,
        paths:str|PathLike[str]|Sequence[str]|Sequence[PathLike[str]]|None=None,
        root:str|None=None,
        params:Mapping|None=None
    ) -> None:
        """ Initialize this object.

        :param paths: one or more config file paths to load
        :type paths: str|PathLike[str]|Sequence[str]|Sequence[PathLike[str]]|None
        :param root: place config values at this root
        :type root: str|None
        :param params: mapping of parameter substitutions
        :type params: Mapping|None
        """
        super().__init__()
        if paths:
            self.load(paths, root, params)

    def load(self,
        paths:str|PathLike[str]|Sequence[str]|Sequence[PathLike[str]],
        root:str|None=None,
        params:Mapping|None=None
    ) -> None:
        """ Load data from configuration files.

        Configuration values are read from a sequence of one or more TOML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value. If a root is specified the config data
        will be loaded under that attribute.

        :param paths: one or more config file paths to load
        :type paths: str|PathLike[str]|Sequence[str]|Sequence[PathLike[str]]
        :param root: place config values at this root
        :type root: str|None
        :param params: mapping of parameter substitutions
        :type params: Mapping|None
        """
        sys_paths : list[Path] = []
        if type(paths) in (str, PathLike[str]):
            sys_paths = [Path(paths)]
        elif type(paths) in (Sequence[str], Sequence[PathLike[str]]):
            # assume sequence contains str|PathLike[str]
            sys_paths = [Path(path) for path in paths]
        if params is None:
            params = {}
        for path in sys_paths:
            # Comments must be stripped prior to template substitution to avoid
            # any unintended semantics such as stray `$` symbols.
            comment = re.compile(r"\s*#.*$", re.MULTILINE)
            with open(path, "rt", encoding="UTF-8") as stream:
                logger.info("Reading config data from '%s'", path)
                conf = comment.sub("", stream.read())
                toml = Template(conf).substitute(params)
                data = tomllib.loads(toml)
            if root:
                self.setdefault(root, {}).update(data)
            else:
                self.update(data)


config = TomlConfig()
