def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


def map_range(value, min1, max1, min2, max2):
    return round(min2 + (value - min1) * (max2 - min2) / (max1 - min1))


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
    """Cycles through integers by shift amount with a constraint from 0 to length.
    Positive shift_amounts will increase the index looping around to zero.
    Negative shift amounts will decrease the index looping around to the index (length - 1)
    """
    if abs(shift_amount) > length:
        shift_amount = shift_amount // length
    newIndex: int = current_index + shift_amount
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


def scroll_bank(array_list: list, bank_amount: int, bank_index: int = 0) -> list:
    """
    Scroll through a list of items in banks of a specified amount.

    :param array_list: List of items to scroll through
    :param bank_amount: Amount of items per bank
    :param bank_index: Index of the bank to view
    :return: List of items in the specified bank

    """
    total = len(array_list)
    bank_max = total // bank_amount if total > bank_amount else 1
    if total % bank_amount != 0 and total > bank_amount:
        bank_max += 1
    bank_index = bank_index % bank_max
    start = bank_index * bank_amount
    end = start + bank_amount
    return array_list[start:end]
