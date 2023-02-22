from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте длинную ссылку',
        validators=[DataRequired(message='Обязательное поле.'),
                    Length(1, 256)],
    )
    custom_id = URLField(
        'Добавьте короткую ссылку',
        validators=[Optional(), Length(1, 16)]
    )
    submit = SubmitField('Создать')