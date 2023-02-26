
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short(short_id):
    url_map = URLMap.get_by_short_id_or_original(short_id)
    if url_map:
        return jsonify({'url': url_map.to_dict()['url']}), HTTPStatus.OK.value
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND.value)


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    data = request.get_json()
    if data:
        url = URLMap.create(data)
        return jsonify({
            'url': url.to_dict()['url'],
            'short_link': f"{request.host_url}{url.to_dict()['custom_id']}"
        }), HTTPStatus.CREATED.value
    raise InvalidAPIUsage('Отсутствует тело запроса')
