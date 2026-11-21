import json
import os
from pathlib import Path
from typing import Any, Dict, Iterator, Mapping, Optional, Union


class ConfigCascade(Mapping[str, Any]):
    """Layered configuration container supporting operator-based defaults merging."""

    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        parent: Optional["ConfigCascade"] = None,
    ):
        self._data = data or {}
        self._parent = parent

    def __getitem__(self, key: str) -> Any:
        if key in self._data:
            return self._data[key]
        if self._parent is not None:
            return self._parent[key]
        raise KeyError(f"Configuration option '{key}' is undefined")

    def __iter__(self) -> Iterator[str]:
        keys = set(self._data.keys())
        if self._parent:
            keys.update(self._parent)
        return iter(keys)

    def __len__(self) -> int:
        return len(set(self))

    def __or__(self, fallback: Union[Dict[str, Any], "ConfigCascade"]) -> "ConfigCascade":
        """Chain defaults using the bitwise OR operator."""
        if isinstance(fallback, dict):
            fallback = ConfigCascade(fallback)
        if isinstance(fallback, ConfigCascade):
            parent_cascade = self._parent | fallback if self._parent else fallback
            return ConfigCascade(self._data, parent=parent_cascade)
        return self

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as err:
            raise AttributeError(err) from err

    @classmethod
    def from_env(cls, prefix: str = "CONFIG_") -> "ConfigCascade":
        env_data = {}
        for k, v in os.environ.items():
            if k.startswith(prefix):
                clean_key = k[len(prefix) :].lower()
                try:
                    env_data[clean_key] = json.loads(v)
                except (json.JSONDecodeError, TypeError):
                    env_data[clean_key] = v
        return cls(env_data)

    @classmethod
    def from_file(cls, filepath: Union[str, Path]) -> "ConfigCascade":
        path = Path(filepath)
        if not path.exists():
            return cls()
        with path.open("r", encoding="utf-8") as file:
            return cls(json.load(file))
