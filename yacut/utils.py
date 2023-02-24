import random
import string
from http import HTTPStatus

from flask import abort

from .models import URLMap

MAX_TRIES = 10
SHORT_ID_LENGTH = 6


def get_unique_short_id():
    chars = string.ascii_letters + string.digits
    for _ in range(MAX_TRIES):
        random_url = ''.join(
            random.choice(chars) for _ in range(SHORT_ID_LENGTH))
    if not URLMap.query.filter_by(short=random_url).first():
        return random_url
    abort(HTTPStatus.INTERNAL_SERVER_ERROR.value)