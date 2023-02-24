import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short(short_id):
    url_map = URLMap.get_by_short_id_or_original(short_id)
    if url_map:
        return jsonify({'url': url_map.to_dict()['url']}), HTTPStatus.OK.value
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND.value)


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    pattern = r'^[a-zA-Z0-9_]{1,16}$'
    data = request.get_json()
    if data:
        if 'url' not in data:
            raise InvalidAPIUsage('"url" является обязательным полем!')
        url = URLMap.get_by_short_id_or_original(data['url'])
        if url and 'custom_id' not in data:
            url.short = get_unique_short_id()
        elif ('custom_id' in data and
              data['custom_id'] != '' and
              data['custom_id'] is not None):
            if not re.match(pattern, data['custom_id']):
                raise InvalidAPIUsage('Указано недопустимое имя для '
                                      'короткой ссылки')
            if URLMap.get_by_short_id_or_original(data['custom_id']):
                error = data['custom_id']
                raise InvalidAPIUsage(f'Имя "{error}" уже занято.')
            if url:
                url.short = data['custom_id']
            else:
                url = URLMap(
                    original=data['url'],
                    short=data['custom_id']
                )
                URLMap.add(url)
        else:
            url = URLMap(
                original=data['url'],
                short=get_unique_short_id()
            )
            URLMap.add(url)
        URLMap.commit()
        return jsonify({
            'url': url.to_dict()['url'],
            'short_link': f"{request.host_url}{url.to_dict()['custom_id']}"
        }), HTTPStatus.CREATED.value
    raise InvalidAPIUsage('Отсутствует тело запроса')
