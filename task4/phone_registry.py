from typing import Dict, Tuple, List, Optional

registry: Dict[str, str] = {}

def save_phone(name: str, number: str):
    registry[name] = number

def find_phone(name: str) -> Optional[str]:
    return registry.get(name)

def get_all_saved_phones() -> List[Tuple[str, str]]:
    return list(registry.items())