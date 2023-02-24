

from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        original_link = form.original_link.data
        url = URLMap.get_by_short_id_or_original(original_link)
        if url and custom_id == '':
            url.short = get_unique_short_id()
        elif custom_id != '' and custom_id is not None:
            if URLMap.get_by_short_id_or_original(custom_id):
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
    url = URLMap.get_by_short_id_or_original(short)
    if url:
        return redirect(url.original)
    abort(HTTPStatus.NOT_FOUND.value)