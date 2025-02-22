from flask import render_template, request, redirect, url_for, jsonify, current_app, send_from_directory, flash, session
from flask_login import login_required
from app.projects import bp
from app.extensions import db
from app.projects.project import Project
from app.projects.task import Task
from app.projects.event import Event
from app.projects.note import Note
from app.projects.file import File
from datetime import datetime, timedelta
import os
import uuid


@bp.route('/')
@login_required
def index():
    projects = Project.query.order_by(Project.category, Project.name).all()
    if session.get("selected_starred_projects_tab") and request.args.get("change_tab", "0") == "0":
        return redirect(url_for("projects.index_starred"))
    show_starred = 0
    session["selected_starred_projects_tab"] = 0
    projects_by_category = {}
    for project in projects:
        category = project.category
        if category not in projects_by_category:
            projects_by_category[category] = []
        projects_by_category[category].append(project)
    return render_template('projects/index.html', projects=projects, projects_by_category=projects_by_category, show_starred=show_starred)
@bp.route('/starred')
@login_required
def index_starred():
    projects = Project.query.filter_by(starred = 1).order_by(Project.category, Project.name).all()
    show_starred = 1
    session["selected_starred_projects_tab"] = 1
    projects_by_category = {}
    for project in projects:
        category = project.category
        if category not in projects_by_category:
            projects_by_category[category] = []
        projects_by_category[category].append(project)
    return render_template('projects/index.html', projects=projects, projects_by_category=projects_by_category, show_starred=show_starred)
@bp.route('/store', methods=["POST"])
@login_required
def store():
    project = Project(name=request.form["name"], status_text = "")
    db.session.add(project)
    db.session.commit()
    return redirect(url_for("projects.index"))
@bp.route('/<id>')
@login_required
def show(id):
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.order_by(Project.category, Project.name).filter_by(category = project.category)
    project.status_text = project.status_text.replace("\\", "\\\\")
    return render_template('projects/show.html', projects=projects, project=project)
@bp.route('/<id>/star', methods=["POST"])
@login_required
def star_projects(id):
    project = Project.query.filter_by(id = request.form["project_id"]).first_or_404()
    project.starred = not project.starred
    db.session.commit()
    return jsonify({"status": "success", "starred": project.starred})
@bp.route('/<id>/tasks')
@login_required
def show_tasks(id):
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.order_by(Project.category, Project.name).filter_by(category = project.category)
    return render_template('projects/show-tasks.html', projects=projects, project=project)
@bp.route('/<id>/update', methods=["POST"])
@login_required
def update(id):
    project = Project.query.filter_by(id = id).first_or_404()
    if "name" in request.form:
        project.name = request.form["name"]
    if "status_text" in request.form:
        project.status_text = request.form["status_text"]
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
@bp.route('/<id>/tasks/star', methods=["POST"])
@login_required
def star_tasks(id):
    task = Task.query.filter_by(id = request.form["task_id"]).first_or_404()
    task.starred = not task.starred
    db.session.commit()
    return jsonify({"status": "success", "starred": task.starred})
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
    projects = Project.query.order_by(Project.category, Project.name).filter_by(category = project.category)
    return render_template('projects/show-events.html', projects=projects, project=project)
@bp.route('/<id>/events/get')
@login_required
def events_get(id):
    events = Event.query.all()
    events_list = []
    for event in events:
        color = "#303133"
        if id != 0:
            if (str(event.project_id) == str(id)):
                color = "#112b96"
        if(event.all_day):
            event.end += timedelta(days = 1)
            start = event.start.strftime('%Y-%m-%d')
            end = event.end.strftime('%Y-%m-%d')
        else:
            start = event.start.strftime('%Y-%m-%dT%H:%M:%S')
            end = event.end.strftime('%Y-%m-%dT%H:%M:%S')
        events_list.append({
                'id': event.id,
                'title': event.name,
                'start': start,
                'end': end,
                'project_name': Project.query.filter_by(id = event.project_id).first().name,
                'project_url': url_for("projects.show", id = event.project_id),
                'color': color,
                'location': event.location,
                'travel_time': event.travel_time

            })
    return jsonify(events_list)
@bp.route('/<id>/events/store', methods=["POST"])
@login_required
def events_store(id):
    event = Event(project_id = id, name=request.form["title"], start = datetime.strptime(request.form["start"], '%Y-%m-%dT%H:%M:%S%z'), end = datetime.strptime(request.form["end"], '%Y-%m-%dT%H:%M:%S%z'), all_day=int(request.form["all-day"]))
    db.session.add(event)
    db.session.commit()
    return jsonify({"status": "success"})
@bp.route('/<id>/events/update', methods=["POST"])
@login_required
def events_update(id):
    event = Event.query.filter_by(id = request.form["id"]).first_or_404()
    event.name=request.form["title"]
    event.location=request.form["location"]
    event.travel_time=request.form["travel_time"]
    event.start = datetime.strptime(request.form["start"], '%Y-%m-%dT%H:%M:%S%z')
    event.end = datetime.strptime(request.form["end"], '%Y-%m-%dT%H:%M:%S%z')
    event.all_day=int(request.form["all_day"])
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
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.order_by(Project.category, Project.name).filter_by(category = project.category)
    return render_template('projects/show-notes.html', projects=projects, project=project)
@bp.route('/<id>/notes/<note_id>')
@login_required
def notes_edit(id, note_id):
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.order_by(Project.category, Project.name).order_by(Project.category, Project.name).filter_by(category = project.category)
    note = Note.query.filter_by(id = note_id).first_or_404()
    note.content = note.content.replace("\\", "\\\\")
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
    db.session.commit()
    return redirect(url_for("projects.show", id = id))
@bp.route('/<id>/files')
@login_required
def files(id):
    files = File.query.filter_by(project_id = id)
    project = Project.query.filter_by(id = id).first_or_404()
    projects = Project.query.order_by(Project.category, Project.name).filter_by(category = project.category)
    return render_template('projects/show-files.html', files=files, project=project, projects=projects)
@bp.route('/<id>/files/upload', methods=["POST"])
@login_required
def files_upload(id):
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file found"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected"})
    if file:
        ext = os.path.splitext(file.filename)[1]  # Pobiera rozszerzenie pliku
        unique_name = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(current_app.static_folder + "/uploads", unique_name)
        db_file = File(name=file.filename, project_id = id, path = unique_name)
        db.session.add(db_file)
        db.session.commit()
        file.save(filepath)
        return redirect(url_for('projects.files', id = id))
@bp.route('/<id>/files/url', methods=["POST"])
@login_required
def files_url(id):
    db_file = File(name=request.form["name"], project_id = id, path = request.form["url"], url = 1)
    db.session.add(db_file)
    db.session.commit()
    return redirect(url_for('projects.files', id = id))
@bp.route('/<id>/files/download/<file_id>')
@login_required
def files_download(id, file_id):
    file_record = File.query.filter_by(id=file_id).first()
    if file_record:
        if os.path.exists(current_app.static_folder + "/uploads/"+file_record.path):
            return send_from_directory(current_app.static_folder + "/uploads", file_record.path, as_attachment=True, download_name=file_record.name)
        else:
            flash("File does not exists", "danger")
    else:
        flash("File not found in database", "danger")
    return redirect(url_for('projects.files', id = id))
@bp.route('/<id>/files/show/<file_id>')
@login_required
def files_show(id, file_id):
    file_record = File.query.filter_by(id=file_id).first()
    if file_record:
        if file_record.url:
            return redirect(file_record.path)
        elif os.path.exists(current_app.static_folder + "/uploads/"+file_record.path):
            return send_from_directory(current_app.static_folder + "/uploads", file_record.path, as_attachment=False, download_name=file_record.name)
        else:
            flash("File does not exists", "danger")
    else:
        flash("File not found in database", "danger")
    return redirect(url_for('projects.files', id = id))
@bp.route('/<id>/files/delete/<file_id>', methods=["POST"])
@login_required
def files_delete(id, file_id):
    file_record = File.query.filter_by(id=file_id).first()
    if file_record:
        if os.path.exists(current_app.static_folder + "/uploads/"+file_record.path):
            #print(os.path.join(current_app.static_folder, "uploads"))
            #print(os.path.join(os.path.join(current_app.static_folder, "uploads"), file_record.path))
            os.remove(os.path.join(os.path.join(current_app.static_folder, "uploads"), file_record.path))
            flash("File successfully deleted.", "success")
        else:
            flash("File does not exists", "danger")
        db.session.delete(file_record)
        db.session.commit()
    else:
        flash("File not found in database", "danger")
    return jsonify({"status": "success"})
@bp.route('/<id>/files/update/<file_id>', methods=["POST"])
@login_required
def files_update(id, file_id):
    file = File.query.filter_by(id=file_id).first()
    file.name = request.form["file_name"]
    db.session.commit()
    return jsonify({"status": "success"})

