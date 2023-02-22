import random
import string

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLForm
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
    abort(500)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        original_link = form.original_link.data
        url = URLMap.query.filter_by(original=original_link).first()
        if url and custom_id == '':
            url.short = get_unique_short_id()
        elif custom_id != '' and custom_id is not None:
            if URLMap.query.filter_by(short=custom_id).first():
                flash(f'Имя {custom_id} уже занято!', '')
                return render_template('yacut.html', form=form)
            if url:
                url.short = custom_id
            else:
                url = URLMap(
                    original=original_link,
                    short=form.custom_id.data
                )
                db.session.add(url)
        else:
            url = URLMap(
                original=original_link,
                short=get_unique_short_id()
            )
            db.session.add(url)
        db.session.commit()
        flash('Ваша новая короткая ссылка:', f'{url.short}')
        form.original_link.data, form.custom_id.data = None, None
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)