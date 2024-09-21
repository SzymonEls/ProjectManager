from app.extensions import db
from app.projects.task import Task

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status_text = db.Column(db.Text)
    tasks = db.relationship('Task', backref='project')
    notes = db.relationship('Note', backref='project')

    def __repr__(self):
        return f'<Project "{self.title}">'