from videocard_parsing.constants import MAX_PRICE, AVAILABLE_STATUSES


def is_cheaper_then_max(price):
    return True if int(price) <= MAX_PRICE else False


def is_available(availability):
    return True if availability in AVAILABLE_STATUSES else False
