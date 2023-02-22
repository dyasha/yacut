from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import is_valid_short_id, is_valid_short_id_len
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map:
        return jsonify({'url': url_map.to_dict()['url']}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    data = request.get_json()
    if data:
        if 'url' not in data:
            raise InvalidAPIUsage('"url" является обязательным полем!')
        url = URLMap.query.filter_by(original=data['url']).first()
        if url and 'custom_id' not in data:
            url.short = get_unique_short_id()
        elif ('custom_id' in data and
              data['custom_id'] != '' and
              data['custom_id'] is not None):
            if (not is_valid_short_id(data['custom_id']) or
                    not is_valid_short_id_len(data['custom_id'])):
                raise InvalidAPIUsage('Указано недопустимое имя для '
                                      'короткой ссылки')
            if URLMap.query.filter_by(short=data['custom_id']).first():
                error = data['custom_id']
                raise InvalidAPIUsage(f'Имя "{error}" уже занято.')
            if url:
                url.short = data['custom_id']
            else:
                url = URLMap(
                    original=data['url'],
                    short=data['custom_id']
                )
                db.session.add(url)
        else:
            url = URLMap(
                original=data['url'],
                short=get_unique_short_id()
            )
            db.session.add(url)
        db.session.commit()
        return jsonify({
            'url': url.to_dict()['url'],
            'short_link': f"{request.host_url}{url.to_dict()['custom_id']}"
        }), 201
    raise InvalidAPIUsage('Отсутствует тело запроса')
