import functools
import logging
from typing import Any, Callable, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dev-toolkit-49')

class DataPipeline:
    def __init__(self):
        self._registry: Dict[str, Callable] = {}

    def register(self, name: str):
        def decorator(func: Callable):
            self._registry[name] = func
            return func
        return decorator

    def execute(self, task: str, *args, **kwargs) -> Any:
        func = self._registry.get(task)
        if not func:
            logger.error(f'Task {task} missing in registry')
            return None
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f'Failure during {task}: {e}')
            return None

pipeline = DataPipeline()

@pipeline.register('clean')
def clean_data(data: str) -> str:
    return ''.join(c for c in data if c.isalnum()).lower()

@pipeline.register('normalize')
def normalize_data(data: str) -> str:
    return data.strip().capitalize()

if __name__ == '__main__':
    raw = '  Dev-Toolkit 49!  '
    cleaned = pipeline.execute('clean', raw)
    result = pipeline.execute('normalize', cleaned)
    print(f'Processed: {result}')