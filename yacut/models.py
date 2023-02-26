import re
from datetime import datetime

from settings import PATTERN
from yacut import db

from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short_id


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(255), unique=True)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            custom_id=self.short,
        )

    @staticmethod
    def add(url):
        db.session.add(url)

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def get_by_short_id_or_original(short_id=None, original=None):
        if short_id:
            return URLMap.query.filter_by(short=short_id).first()
        elif original:
            return URLMap.query.filter_by(original=original).first()

    @staticmethod
    def create(data):
        if 'url' not in data:
            raise InvalidAPIUsage('"url" является обязательным полем!')
        url = URLMap.get_by_short_id_or_original(data['url'])
        if url and 'custom_id' not in data:
            url.short = get_unique_short_id()
        elif ('custom_id' in data and
              data['custom_id'] != '' and
              data['custom_id'] is not None):
            if not re.match(PATTERN, data['custom_id']):
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
        return url
