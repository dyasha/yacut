import random
import string


MAX_TRIES = 10
SHORT_ID_LENGTH = 6


def get_unique_short_id():
    chars = string.ascii_letters + string.digits
    for _ in range(MAX_TRIES):
        return ''.join(
            random.choice(chars) for _ in range(SHORT_ID_LENGTH))
