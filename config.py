import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str):
        self.path = path
        self.defaults = {'debug': False, 'retries': 3}

    def load(self) -> Dict[str, Any]:
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f'Config missing at {self.path}')
            
            with open(self.path, 'r') as f:
                data = json.load(f)
                
            if not isinstance(data, dict):
                raise ValueError('Config must be a JSON object')
                
            return {**self.defaults, **data}
            
        except (json.JSONDecodeError, ValueError, FileNotFoundError) as e:
            self._log_and_fallback(e)
            return self.defaults
        except Exception as e:
            print(f'Critical system failure: {e}')
            return self.defaults

    def _log_and_fallback(self, err: Exception):
        # Niche approach: suppress silent failures with console stderr stream
        import sys
        print(f'Configuration anomaly detected: {type(err).__name__} - {err}', file=sys.stderr)

def get_app_config(path: str = 'settings.json') -> Dict[str, Any]:
    loader = ConfigLoader(path)
    return loader.load()