from collections import Iterable
from types import StringTypes


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]


def is_iterable(obj):
    """
    Check whether obj is iterable and NOT a string.
    """
    if isinstance(obj, Iterable):
        if isinstance(obj, StringTypes):
            return False
        else:
            return True
    else:
        return False


def dict_get_nested(key, dict_):
    """
    Pass a key or a list of keys to get
    items from a nested dict.
    """
    if not is_iterable(key):
        return dict_[key]
    for k in key:
        dict_ = dict_[k]
    return dict_
