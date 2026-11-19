import functools
from typing import Any, Callable, Dict, List, Union

class DataTransformer:
    def __init__(self, data: Union[List, Dict]):
        self._data = data

    def morph(self, pipeline: List[Callable]) -> Any:
        return functools.reduce(lambda d, f: f(d), pipeline, self._data)

def flatten_deep(structure: Any) -> List:
    """recursive transformation of nested structures into linear list"""
    flat = []
    if isinstance(structure, (list, tuple, set)):
        for item in structure:
            flat.extend(flatten_deep(item))
    else:
        flat.append(structure)
    return flat

def alias_mapper(mapping: Dict[str, str]) -> Callable:
    """functional factory for dictionary key substitution"""
    def processor(data: Dict) -> Dict:
        return {mapping.get(k, k): v for k, v in data.items()}
    return processor

def sanitize_stream(data: Dict) -> Dict:
    """stripping of null and empty container values"""
    return {
        k: v for k, v in data.items() 
        if v is not None and (not hasattr(v, '__len__') or len(v) > 0)
    }

if __name__ == '__main__':
    sample = {'user_id': 123, 'meta': None, 'tags': []}
    pipeline = [sanitize_stream, alias_mapper({'user_id': 'id'})]
    result = DataTransformer(sample).morph(pipeline)
    print(result)