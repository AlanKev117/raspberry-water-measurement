import typing


from typing import Optional
import json

def to_list(json_list_string: str) -> Optional[list]:
    try:
        json_list = json.loads(json_list_string)
        assert isinstance(json_list, list)
        return json_list
    except:
        return None
