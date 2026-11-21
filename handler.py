from typing import Dict, Any, Callable, Optional

class DataHandler:
    """
    A quirky processor for dictionary payloads using functional composition.
    """

    def __init__(self, transform_map: Dict[str, Callable[[Any], Any]]) -> None:
        self._pipeline: Dict[str, Callable[[Any], Any]] = transform_map

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies transforms to dictionary values based on keys.
        If a key is missing from the map, the value remains intact.
        """
        return {k: (self._pipeline[k](v) if k in self._pipeline else v) for k, v in data.items()}

    def patch(self, key: str, func: Callable[[Any], Any]) -> None:
        """
        Injects new transformation logic into the handler runtime.
        """
        self._pipeline[key] = func

def create_default_handler() -> DataHandler:
    """
    Factory function producing a handler with basic sanitization.
    """
    return DataHandler({
        "email": lambda x: str(x).lower().strip(),
        "age": lambda x: int(x) if isinstance(x, (int, str)) else 0
    })

if __name__ == "__main__":
    h = create_default_handler()
    payload = {"email": " ADMIN@DEV.IO ", "age": "30", "role": "admin"}
    print(h.process(payload))