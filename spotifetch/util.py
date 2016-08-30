from collections import Iterable
from types import StringTypes


def chunked(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]


def iter_chunked(iterator, chunk_size):
    """
    Same as chunked, but also works on generators.
    This exhausts the generator.
    """
    chunk = []
    for item in iterator:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk



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


def shrink_nested_list(nest, limit=5000):
    """
    The last element from the largest list in
    the nested list is removed until the
    total length of the nest is <= limit.
    """
    nest_len = sum([len(l) for l in nest])
    while nest_len > limit:
        biggest = max(enumerate(nest), key=lambda tup: len(tup[1]))[1]
        biggest.pop()
        nest_len -= 1
    return nest
