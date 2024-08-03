from flask import render_template
from app.main import bp
from app.projects.task import Task
from datetime import datetime


@bp.route('/')
def index():
    return render_template('index.html')
@bp.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks-all.html', tasks=tasks)
@bp.route('/tasks/today')
def tasks_today():
    tasks = Task.query.filter_by(due_date = datetime.today().strftime('%Y-%m-%d'))
    return render_template('tasks-today.html', tasks=tasks)