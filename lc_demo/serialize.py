from __future__ import annotations
from dataclasses import is_dataclass
from lc_demo.serialize_common import TYPE_KEY

def serialize(obj: object):
    if isinstance(obj, (int, float, str, bool)):
        return obj
    elif obj == None:
        return None
    elif isinstance(obj, dict):
        res = {}
        for key in obj.keys():
            value = serialize(obj[key])
            res[key] = value
        return res
    elif isinstance(obj, list):
        res = []
        for elt in obj:
            res.append(serialize(elt))
        return res
    elif is_dataclass(obj):
        return serialize_dataclass(obj)

def serialize_dataclass(obj: object):
    res = {}
    field_names = obj.__annotations__
    for key in field_names.keys():
        value = serialize(getattr(obj, key))
        res[key] = value
    type_name = obj.__class__.__name__
    res[TYPE_KEY] = type_name
    return res
