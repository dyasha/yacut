from flask_wtf import FlaskForm
from settings import ONE_DIGIT, SIXTEEN_DIGIT, TWO_HUND_FIFTY_SIX_DIGIT
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте длинную ссылку',
        validators=[DataRequired(message='Обязательное поле.'),
                    Length(ONE_DIGIT, TWO_HUND_FIFTY_SIX_DIGIT)],
    )
    custom_id = URLField(
        'Добавьте короткую ссылку',
        validators=[Optional(), Length(ONE_DIGIT, SIXTEEN_DIGIT)]
    )
    submit = SubmitField('Создать')