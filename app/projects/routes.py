from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_required
from app.projects import bp
from app.extensions import db
from app.projects.project import Project
from app.projects.task import Task
from app.projects.event import Event
from app.projects.note import Note
from datetime import datetime, timedelta


@bp.route('/')
@login_required
def index():
    projects = Project.query.all()

    projects_by_category = {}
    for project in projects:
        category = project.category
        if category not in projects_by_category:
            projects_by_category[category] = []
        projects_by_category[category].append(project)
    return render_template('projects/index.html', projects=projects, projects_by_category=projects_by_category)
@bp.route('/store', methods=["POST"])
@login_required
def store():
    print(request.form["name"])
    project = Project(name=request.form["name"], status_text = "")
    db.session.add(project)
    db.session.commit()
    return redirect(url_for("projects.index"))
@bp.route('/<id>')
@login_required
def show(id):
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.filter_by(category = project.category)

    return render_template('projects/show.html', projects=projects, project=project)
@bp.route('/<id>/tasks')
@login_required
def show_tasks(id):
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.filter_by(category = project.category)
    return render_template('projects/show-tasks.html', projects=projects, project=project)
@bp.route('/<id>/update', methods=["POST"])
@login_required
def update(id):
    project = Project.query.filter_by(id = id).first_or_404()
    if "name" in request.form:
        project.name = request.form["name"]
    if "status_text" in request.form:
        project.status_text = request.form["status_text"]
    #print(request)
    db.session.commit()
    return redirect(url_for('projects.show', id = id))
@bp.route('/<id>/tasks/store', methods=["POST"])
@login_required
def store_tasks(id):
    task = Task(name = request.form["name"], project_id = id, due_date = datetime.strptime(request.form["date"], "%Y-%m-%d").date())
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('projects.show_tasks', id = id))
@bp.route('/<project_id>/tasks/<task_id>/update', methods=["POST"])
@login_required
def update_tasks(project_id, task_id):
    task = Task.query.filter_by(id = task_id).first_or_404()
    if request.form["task_date"] != "":
        task.due_date = datetime.strptime(request.form["task_date"], "%Y-%m-%d").date()
    if request.form["task_name"] != "":
        task.name = request.form["task_name"]
    db.session.commit()
    return jsonify({"status": "success"})
@bp.route('/<id>/tasks/delete', methods=["POST"])
@login_required
def delete_tasks(id):
    task = Task.query.filter_by(id = request.form["task_id"]).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"status": "success"})
@bp.route('/<id>/events')
@login_required
def events(id):
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.filter_by(category = project.category)
    return render_template('projects/show-events.html', projects=projects, project=project)
@bp.route('/<id>/events/get')
@login_required
def events_get(id):
    if id == "0":
        events = Event.query.all()
    else:
        events = Event.query.filter_by(project_id = id).all()
    events_list = []
    for event in events:
        if(event.all_day):
            event.end += timedelta(days = 1)
            events_list.append({
                'id': event.id,
                'title': event.name,
                'start': event.start.strftime('%Y-%m-%d'),
                'end': event.end.strftime('%Y-%m-%d')
            })    
        else:
            events_list.append({
                'id': event.id,
                'title': event.name,
                'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': event.end.strftime('%Y-%m-%dT%H:%M:%S')
            })
    return jsonify(events_list)
@bp.route('/<id>/events/store', methods=["POST"])
@login_required
def events_store(id):
    event = Event(project_id = id, name=request.form["title"], start = datetime.strptime(request.form["start"], '%Y-%m-%dT%H:%M:%S%z'), end = datetime.strptime(request.form["end"], '%Y-%m-%dT%H:%M:%S%z'), all_day=int(request.form["all-day"]))
    print(event.start)
    db.session.add(event)
    db.session.commit()
    return jsonify({"status": "success"})
@bp.route('/<id>/events/update', methods=["POST"])
@login_required
def events_update(id):
    event = Event.query.filter_by(id = request.form["id"]).first_or_404()
    event.name=request.form["title"]
    event.start = datetime.strptime(request.form["start"], '%Y-%m-%dT%H:%M:%S%z')
    event.end = datetime.strptime(request.form["end"], '%Y-%m-%dT%H:%M:%S%z')
    event.all_day=int(request.form["all_day"])
    print(event.start)
    db.session.commit()
    return jsonify({"status": "success"})
@bp.route('/<id>/events/delete', methods=["POST"])
@login_required
def events_delete(id):
    event = Event.query.filter_by(id = request.form["id"]).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return jsonify({"status": "success"})
@bp.route('/<id>/notes')
@login_required
def notes(id):
    projects = Project.query.all()
    project = Project.query.filter_by(id = id).first_or_404()
    return render_template('projects/show-notes.html', projects=projects, project=project)
@bp.route('/<id>/notes/<note_id>')
@login_required
def notes_edit(id, note_id):
    projects = Project.query.all()
    project = Project.query.filter_by(id = id).first_or_404()
    note = Note.query.filter_by(id = note_id).first_or_404()
    return render_template('projects/notes-edit.html', projects=projects, project=project, note=note)
@bp.route('/<id>/notes/new')
@login_required
def notes_create(id):
    note = Note(name = "New note", content = "", project_id = id)
    db.session.add(note)
    db.session.commit()
    return redirect(url_for("projects.notes_edit", id = id, note_id = note.id))
@bp.route('/<id>/notes/update', methods=["POST"])
@login_required
def notes_update(id):
    note = Note.query.filter_by(id = request.form["note_id"]).first_or_404()
    if "name" in request.form:
        note.name = request.form["name"]
    if "content" in request.form:
        note.content = request.form["content"]
    db.session.commit()
    return jsonify({"status": "success"})
@bp.route('/<id>/projects/update-category', methods=["POST"])
@login_required
def update_category(id):
    project = Project.query.filter_by(id = id).first_or_404()
    project.category = request.form["category"]
    print(project.category)
    db.session.commit()
    return redirect(url_for("projects.show", id = id))


