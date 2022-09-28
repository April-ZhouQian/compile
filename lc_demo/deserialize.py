import typing
import typing_extensions
from lc_demo.serialize_common import TYPE_KEY

def deserialize_dataclass(x: dict[str, typing.Any], type_map: dict[str, type]):
    cls = type_map[x[TYPE_KEY]]
    fields = {}
    for field_name in x.keys():
        if field_name == TYPE_KEY:
            break
        field_value = deserialize(x[field_name], type_map)
        fields[field_name] = field_value
    obj = cls(**fields)
    return obj

def deserialize(x, type_map: dict[str, type]):
    if isinstance(x, (int, float, bool, str)):
        return x
    elif x == None:
        return None
    elif isinstance(x, list):
        res = []
        for elt in x:
            res.append(deserialize(elt, type_map))
        return res
    elif isinstance(x, dict):
        if  TYPE_KEY in x:
            obj = deserialize_dataclass(x, type_map)
            return obj
        res = {}
        for key in x.keys():
            res[key] = deserialize(x[key], type_map)
    else:
        if typing.TYPE_CHECKING:
            typing_extensions.assert_never(x)
        else:
            assert False, x

