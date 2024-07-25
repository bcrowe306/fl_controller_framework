def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


def get_index(list, name):
    for index, item in enumerate(list):
        if item.name == name:
            return index
    else:
        return -1

def safe_getattr(obj, name, default=None):
    try:
        return getattr(obj, name, default)
    except Exception:  # or your specific exceptions
        return default


def cycle_bounds(current_index: int, length: int, shift_amount: int) -> int:
    """ Cycles through integers by shift amount with a constraint from 0 to length. 
        Positive shift_amounts will increase the index looping around to zero.
        Negative shift amounts will decrease the index looping around to the index (length - 1)
    """
    last_index: int = length - 1
    if shift_amount < 0:
        newIndex = current_index + shift_amount
    if newIndex >= length:
        newIndex = newIndex % length
    if newIndex < 0:
        newIndex = length + shift_amount
    return newIndex


def limit_range(new_index: int, lower_limit: int, upper_limit: int) -> int:
    """
    Returns the new_index limited to the defined upper and lower limit. This will keep new_index in that defined range
    """
    if new_index > upper_limit:
        new_index = upper_limit
    if new_index < lower_limit:
        new_index = lower_limit
    return new_index


def limit_bounds(new_index: int, length: int) -> int:
    """
    Returns the new_index limited to the length-1. This will keep new_index between 0 <-> (length - 1)
        Useful for indexing in lists without violating the list bounds
    """
    last_index = length - 1
    if new_index > last_index:
        new_index = last_index
    if new_index < 0:
        new_index = 0
    return new_index
