import functools
from typing import Any, Callable, List, Dict

class DataPipeline:
    def __init__(self, steps: List[Callable] = None):
        self.steps = steps or []

    def add_stage(self, func: Callable) -> None:
        self.steps.append(func)

    def execute(self, data: Any) -> Any:
        return functools.reduce(lambda acc, func: func(acc), self.steps, data)

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k).strip().lower(): v for k, v in data.items() if v is not None}

def transform_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    data.update({'processed': True, 'version': 49})
    return data

def run_dev_toolkit_flow(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    pipeline = DataPipeline([sanitize_input, transform_payload])
    return pipeline.execute(raw_data)

if __name__ == '__main__':
    sample = {' NAME ': 'dev-toolkit', 'VAL': None, 'ID': 49}
    print(run_dev_toolkit_flow(sample))