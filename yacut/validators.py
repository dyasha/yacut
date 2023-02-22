import re


def is_valid_short_id(short_id):
    if not short_id:
        return False
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, short_id) is not None

def is_valid_short_id_len(short_id):
    if len(short_id) < 16:
        return short_id is not None