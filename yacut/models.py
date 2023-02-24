from datetime import datetime

from yacut import db


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
        else:
            raise ValueError('Не указан short_id или original')
