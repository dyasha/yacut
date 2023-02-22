import random
import string


def generate_short_id(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

print(generate_short_id())
