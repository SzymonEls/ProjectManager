from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.main import bp
from app.extensions import db
from app.main.user import User
from app.projects.task import Task
from app.projects.project import Project
from app.projects.event import Event
from datetime import datetime

@bp.route('/tasks')
@login_required
def tasks():
    tasks = Task.query.all()
    return render_template('tasks-all.html', tasks=tasks)
@bp.route('/tasks/today')
@login_required
def tasks_today():
    tasks = Task.query.filter_by(due_date = datetime.today().strftime('%Y-%m-%d'))
    return render_template('tasks-today.html', tasks=tasks)
@bp.route('/events')
@login_required
def events():
    id = 1
    projects = Project.query.all()
    project = Project.query.filter_by(id = id).first_or_404()
    return render_template('events.html', projects=projects, project=project)
@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('projects.index'))

        flash('Invalid username or password.', category="warning")
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form["password"] == request.form["confirm-password"]:
            existing_user = User.query.filter_by(username=request.form["username"]).first()
            if existing_user is None:
                username = request.form.get('username')
                password = request.form.get('password')
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Registered successfully. You can login now.", category="success")
            else:
                flash('Username already taken, please choose another one.', 'warning')
                return redirect(url_for('main.register'))

        else:
            flash("Passwords don't match.", category="warning")
            return redirect(url_for('main.register'))

        return redirect(url_for('main.login'))
    return render_template('register.html')
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
@bp.route('/edit-profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        existing_user = User.query.filter_by(username = request.form["username"]).first()
        if existing_user is None or existing_user.username == current_user.username:     
            if request.form["password"] == request.form["confirm-password"] and request.form["password"] != "":
                current_user.username = request.form["username"]
                current_user.password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
                db.session.commit()
                flash("Username and password updated successfully.", category="success")
            elif request.form["password"] == "":
                current_user.username = request.form["username"]
                db.session.commit()
                flash("Username updated successfully.", category="success")
            else:
                flash("Passwords don't match!", category="warning")
        else:
            flash("Username already taken.", category="warning")
    return render_template('edit-profile.html')