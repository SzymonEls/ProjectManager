from flask import render_template, request, redirect, url_for, jsonify
from app.projects import bp
from app.extensions import db
from app.projects.project import Project
from app.projects.task import Task
from datetime import datetime


@bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)
@bp.route('/store', methods=["POST"])
def store():
    project = Project(name=request.form["name"], status_text = "")
    db.session.add(project)
    db.session.commit()
    return redirect(url_for("projects.index"))
@bp.route('/<id>')
def show(id):
    projects = Project.query.all()
    project = Project.query.filter_by(id = id).first_or_404()
    return render_template('projects/show.html', projects=projects, project=project)
@bp.route('/<id>/tasks')
def show_tasks(id):
    projects = Project.query.all()
    project = Project.query.filter_by(id = id).first_or_404()
    return render_template('projects/show-tasks.html', projects=projects, project=project)
@bp.route('/<id>/update', methods=["POST"])
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
def store_tasks(id):
    task = Task(name = request.form["name"], project_id = 1, due_date = datetime.strptime(request.form["date"], "%Y-%m-%d").date())
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('projects.show_tasks', id = id))
@bp.route('/<id>/tasks/delete', methods=["POST"])
def delete_tasks(id):
    task = Task.query.filter_by(id = request.form["task_id"]).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"status": "success"})


