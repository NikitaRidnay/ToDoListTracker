from flask import Flask, jsonify, render_template, redirect, url_for, flash
from models import db, Note
from forms import NoteForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/ToDoList'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SecretKey'

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NoteForm()
    if form.validate_on_submit():
        print("Форма прошла валидацию")  
        new_note = Note(
            content=form.content.data,
            info=form.info.data,
            is_task=form.is_task.data,
            timer=form.timer.data if form.is_task.data else None  
        )
        db.session.add(new_note)
        db.session.commit()
        flash('Заметка добавлена!', 'success')
        return redirect(url_for('index'))
    else:
        print("Форма не прошла валидацию")  
        print(form.errors)  
    notes = Note.query.order_by(Note.id.desc()).all() #от последней к первой #
    completed_count = Note.query.filter_by(is_completed=True).count()
    uncompleted_count = Note.query.filter(Note.is_completed == False, 
                                        Note.is_expired == False).count()
    
    #notes = Note.query.all() - все заметки без фильтрацци 
    return render_template('ints.html', 
                         form=form,
                         notes=notes,
                         completed_count=completed_count,
                         uncompleted_count=uncompleted_count)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Заметка удалена!', 'success')
    return redirect(url_for('index'))

@app.route('/complete_task/<int:note_id>')
def complete_task(note_id):
    note = Note.query.get_or_404(note_id)
    note.is_completed = True
    note.is_expired = False  # Явный сброс обоих статусов
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/uncomplete_task/<int:note_id>', methods=['POST'])
def uncomplete_task(note_id):
    note = Note.query.get_or_404(note_id)
    note.is_completed = False
    note.is_expired = True  # Явный сброс обоих статусов
    db.session.commit()
    flash('Задача отменена!', 'success')  
    return redirect(url_for('index'))


@app.route('/mark_expired/<int:note_id>', methods=['POST'])
def mark_expired(note_id):
    note = Note.query.get_or_404(note_id)
    if not note.is_completed:
        note.is_expired = True
        db.session.commit()
    return jsonify({'status': 'success'})



@app.route('/edit/<int:note_id>', methods=['POST'])
def edit(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteForm()
    if form.validate_on_submit():
        note.content = form.content.data
        note.info = form.info.data
        note.is_task = form.is_task.data
        note.timer = form.timer.data if form.is_task.data else None
        db.session.commit()
        flash('Заметка обновлена!', 'success')
    else:
        flash('Ошибка при обновлении заметки', 'error')
    return redirect(url_for('index'))
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)