from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db
from models import Event
from forms import EventForm
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

init_db()


@app.route('/')
def index():
    db = get_db()
    events = db.query(Event).filter(
        Event.end_datetime >= datetime.now()
    ).order_by(Event.start_datetime.asc()).all()
    return render_template('index.html', events=events)


@app.route('/past')
def past_events():
    db = get_db()
    events = db.query(Event).filter(
        Event.end_datetime < datetime.now()
    ).order_by(Event.start_datetime.desc()).all()
    return render_template('past_events.html', events=events)


@app.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        if form.end_datetime.data < form.start_datetime.data:
            flash('Дата окончания не может быть раньше даты начала!', 'error')
            return render_template('edit_event.html', form=form, title='Добавить событие')

        db = get_db()
        event = Event(
            title=form.title.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data,
            location=form.location.data,
            description=form.description.data
        )
        db.add(event)
        db.commit()
        flash('Событие успешно добавлено!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_event.html', form=form, title='Добавить событие')


@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    db = get_db()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        flash('Событие не найдено!', 'error')
        return redirect(url_for('index'))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        if form.end_datetime.data < form.start_datetime.data:
            flash('Дата окончания не может быть раньше даты начала!', 'error')
            return render_template('edit_event.html', form=form, title='Редактировать событие')

        event.title = form.title.data
        event.start_datetime = form.start_datetime.data
        event.end_datetime = form.end_datetime.data
        event.location = form.location.data
        event.description = form.description.data
        db.commit()
        flash('Событие успешно обновлено!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_event.html', form=form, title='Редактировать событие')


@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    db = get_db()
    event = db.query(Event).filter(Event.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
        flash('Событие удалено!', 'success')
    else:
        flash('Событие не найдено!', 'error')
    return redirect(request.referrer or url_for('index'))


@app.route('/delete_all_past')
def delete_all_past():
    db = get_db()
    count = db.query(Event).filter(Event.end_datetime < datetime.now()).delete()
    db.commit()
    flash(f'Удалено {count} прошедших событий.', 'success')
    return redirect(url_for('past_events'))


if __name__ == '__main__':
    app.run(debug=True)